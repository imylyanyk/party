/**
 * Created by imylyanyk on 9/24/16.
 */
$(document).ready(function() {
    $('#add').click(function() {
       console.log('search... ');
        $.ajax({
            url: '/ajax_search',
            data: {q : $('#search_term').val() },
            dataType: 'json',
            success: function(data) {
                console.log('success!');
                for(var i=0;i<data.length;++i) {
                    var obj = $('.search-result-item-template').clone();
                    obj.removeClass('search-result-item-template');
                    obj.addClass('search-result-item');

                    // Prepare data
                    obj.find('.preview').attr('src', data[i].snippet.thumbnails.medium.url);
                    obj.find('.title').html(data[i].snippet.title);
                    obj.find('.title').attr('href', 'https://youtube.com/watch?v=' + data[i].id.videoId);
                    obj.find('.description').html(data[i].snippet.description);
                    obj.find('.publisher').html(data[i].snippet.channelTitle);

                    $('.results').append(obj);
                }
                console.log(data);
            }
        })
    });
});