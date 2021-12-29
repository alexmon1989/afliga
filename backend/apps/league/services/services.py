from apps.league.models import Match, PERIODS_CHOICES
from typing import List, Dict
from itertools import groupby


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

    res = []
    for key, group_items in groupby(events, key=lambda x: x['period']):
        item = {
            'period': next((x[1] for x in PERIODS_CHOICES if x[0] == key), None),
            'items': [],
        }
        for group_item in group_items:
            item['items'].append(group_item)
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
