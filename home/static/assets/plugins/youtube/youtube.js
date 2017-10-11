$(function () {
    var img = document.querySelectorAll('img[src$="/maxresdefault.jpg"]');
    for (var i = 0; i < img.length; i++) {
        img[i].onclick = function () {
            var idImg = this.src.replace(/http...img.youtube.com.vi.(.*?).maxresdefault.jpg/gi, '$1');
            theIframe = document.createElement('iframe');
            theIframe.src = '//www.youtube.com/embed/' + idImg + '?rel=0&autoplay=1';
            theIframe.onclick = function () {
                this.parentElement.removeChild(this);
            };
            this.parentNode.insertBefore(theIframe, this.nextSibling);
        }
    }
});
