$(function(){
    var pages = $('body>div.page');
    pages.prepend('<span class="page-number pull-right"></span>');
    for(var i = 0; i < pages.length; i++){
        var page = $(pages[i]);
        // console.log(page);
        page.attr("id", "page-"+(i+1));
        page.find('.page-number').text(""+(i+1)+"/"+(pages.length));
    }
    for(var i = 0; i < pages.length; i++){
        var page = $(pages[i]);
        page.click((function(){
                    var nextPage = $('#page-'+((i+1)%pages.length+1));
                    return function(e){
                        var top = nextPage.offset().top ;
                        $("html, body").animate({ scrollTop: top}, 500);
                    }
                })());
    }
});
