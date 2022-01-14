from django.db.models import Count, Q
from apps.league.models import Match, Event, PERIODS_CHOICES, Competition, CompetitionTeamApplication, MatchLineup
from typing import List
from afliga.utils import calculate_age


def match_get_all_events(match: Match) -> List:
    """Возвращает события матча, разбитые по таймам."""
    events = match.event_set.select_related(
        'player', 'event_type'
    ).order_by(
        'event_time'
    ).values(
        'event_time',
        'event_type_id',
        'event_type__title',
        'player_id',
        'player__name',
        'player__photo',
        'player_assigned_id',
        'player_assigned__name',
        'team_id',
        'note',
        'period',
    )

    periods = sorted(list(set([x['period'] for x in events])))
    res = []
    for period in periods:
        item = {
            'period': next((x[1] for x in PERIODS_CHOICES if x[0] == period), None),
            'items': [],
        }
        for event in events:
            if event['period'] == period:
                item['items'].append(event)
        res.append(item)

    return res


def match_get_main_events(events: List) -> List:
    """Возвращает события матча без лучших игроков."""
    res = []
    for period in events:
        events_filtered = list(filter(
            lambda x: x['event_type_id'] != 8, period['items']
        ))
        if len(events_filtered) > 0:
            res.append({
                'period': period['period'],
                'items': events_filtered
            })
    return res


def match_get_lineup(match: Match, match_events: List) -> List:
    """Возвращает список заявленных на матч игроков."""
    players = match.matchlineup_set.order_by(
        'player__name'
    ).select_related(
        'player',
    ).values(
        'team_id',
        'player_id',
        'player__name',
        'start',
    )

    # Объединение событий разных таймов
    flatten_events = []
    for period_events in match_events:
        flatten_events.extend(period_events['items'])

    # События матча с игроками
    for player in players:
        player['events'] = []
        for event in flatten_events:
            if (event['player_id'] == player['player_id'] or event['player_assigned_id'] == player['player_id']) \
                    and event['event_type_id'] != 8:
                player['events'].append(event)

        # Сортировка - замены в конце списка
        player['events'].sort(
            key=lambda x: (float('inf') if x['event_type_id'] == 12 else x['event_time'] if x['event_time'] else 0)
        )
    return players


def match_get_lineup_start_team(lineup: List, team_id: int) -> List:
    """Возвращает список игроков определённой команды, вышедших в старте на матч."""
    return list(filter(lambda x: x['team_id'] == team_id and x['start'], lineup))


def match_get_lineup_reserve_team(lineup: List, team_id: int) -> List:
    """Возвращает список игроков определённой команды, заявленных как запасные на матч."""
    return list(filter(lambda x: x['team_id'] == team_id and not x['start'], lineup))


def match_get_goals_team(events: List, team_id: int) -> List:
    """Возвращает список голов и автоголов в матче определённой команды."""
    res = []
    for period in events:
        events_filtered = list(filter(
            lambda x: x['team_id'] == team_id and x['event_type_id'] in (1, 9), period['items']
        ))
        if len(events_filtered) > 0:
            res.extend(events_filtered)

    return res


def match_get_best_players(events: List, team_id: int) -> List:
    """Возвращает лучших игроков матча определённой команды."""
    for period in events:
        events_filtered = list(filter(
            lambda x: x['event_type_id'] == 8 and x['team_id'] == team_id, period['items']
        ))
        if len(events_filtered) > 0:
            return events_filtered
    return []


def match_get_personal_matches_stat(team_1_id: int, team_2_id: int) -> dict:
    """Возвращает историю личных встреч команд."""
    res = {
        'count': 0,
        'team_1': {
            'wins': 0,
            'losses': 0,
            'draws': 0,
        },
        'team_2': {
            'wins': 0,
            'losses': 0,
            'draws': 0,
        },
    }

    # Матчи команд
    matches = Match.objects.filter(
        Q(is_finished=True),
        Q(team_1_id=team_1_id, team_2_id=team_2_id) | Q(team_1_id=team_2_id, team_2_id=team_1_id)
    ).values(
        'team_1_id',
        'team_2_id',
        'goals_team_1',
        'goals_team_2',
    )

    res['count'] = matches.count()

    for match in matches:
        if match['goals_team_1'] == match['goals_team_2']:
            res['team_1']['draws'] += 1
            res['team_2']['draws'] += res['team_1']['draws']
        elif match['goals_team_1'] > match['goals_team_2']:  # Выиграла команда 1
            if match['team_1_id'] == team_1_id:
                res['team_1']['wins'] += 1
                res['team_2']['losses'] += 1
            else:
                res['team_2']['wins'] += 1
                res['team_1']['losses'] += 1
        else:  # Выиграла команда 2
            if match['team_1_id'] == team_1_id:
                res['team_2']['wins'] += 1
                res['team_1']['losses'] += 1
            else:
                res['team_1']['wins'] += 1
                res['team_2']['losses'] += 1

    return res


def competition_get_assistants(competition_id) -> List:
    """Возвращает список ассистентов турнира."""
    players = Event.objects.filter(
        match__competition_id=competition_id,
        event_type=1
    ).values(
        'player_assigned'
    ).annotate(
        num_assistants=Count('player_assigned')
    ).filter(
        num_assistants__gt=0
    ).order_by(
        '-num_assistants',
        'player_assigned__name'
    ).values(
        'player_assigned__pk',
        'player_assigned__name',
        'player_assigned__photo',
        'team__pk',
        'team__title',
        'team__city',
        'team__logo',
        'num_assistants'
    )

    return players


def competition_get_full_title(competition: Competition) -> str:
    """Возвращает полное название сезона (со спонсором)."""
    res = f"{competition.title}: {competition.season.title}"
    if competition.season.sponsor:
        res = f"{res}-{competition.season.sponsor}"
    return res


def competition_get_current_season_items_with_team(team_id: int) -> list:
    """Возвращает соревнования текущего сезона, в которых есть команда
    (с базовой статистикой: игр сыграно, голы, желтые, красные карточки)."""
    competitions = Competition.objects.filter(
        season__is_current_season=True,
        competitionteamapplication__team=team_id
    )

    res = []
    for competition in competitions:
        item = dict()
        item['title'] = competition.title

        # Заявка команды на турнир
        application = CompetitionTeamApplication.objects.filter(
            competition=competition,
            team_id=team_id
        ).first()

        # События турнира с командой
        matches_events = Event.objects.filter(
            Q(match__competition=competition),
            Q(match__team_1_id=team_id) | Q(match__team_2_id=team_id)
        ).exclude(pk__in=(6, 8, 9, 10, 11, 21,)).values('event_type_id', 'player_id')

        # Стартовые составы матчей команды в турнире
        matches_start_line_ups = MatchLineup.objects.filter(
            Q(start=True),
            Q(match__competition=competition),
            Q(match__team_1_id=team_id) | Q(match__team_2_id=team_id)
        ).values('player_id',)

        # Данные игроков заявки
        players_data = []
        for player in application.players.order_by('position').select_related('position'):
            player_data = dict()
            player_data['pk'] = player.pk
            player_data['name'] = player.name
            player_data['age'] = calculate_age(player.birth_date)
            player_data['position'] = player.position.title
            # Количество игр - это сумма игр в стартовом составе и замен
            player_data['games'] = len(
                [x for x in matches_start_line_ups if x['player_id'] == player.pk]
            ) + len(
                [x for x in matches_events if x['player_id'] == player.pk and x['event_type_id'] == 8]
            )
            player_data['goals'] = len(
                [x for x in matches_events if x['player_id'] == player.pk and x['event_type_id'] == 1]
            )
            player_data['yellow_cards'] = len(
                [x for x in matches_events if x['player_id'] == player.pk and x['event_type_id'] == 2]
            )
            player_data['red_cards'] = len(
                [x for x in matches_events if x['player_id'] == player.pk and x['event_type_id'] == 3]
            )

            players_data.append(player_data)

        item['application'] = players_data

        res.append(item)

    return res
