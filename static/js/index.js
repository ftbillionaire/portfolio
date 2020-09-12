"use strict";

$(document).ready(function(){
    $(document).on("submit", "#comment-form", function(e){
        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: '',
            async: true,
            data: {
                name: $('#name').val(),
                body: $('#body').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(json){
                var d = new Date();
                var months = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."];

                $("#comment-form")[0].reset();
                console.log("Comment created!");

                $("#comment-block").prepend(
                    '<div class="mt-3 mb-3 card">' +
                        '<div class="card-header">' +
                            months[d.getMonth()] + ' ' + d.getDate() + ', ' + d.getFullYear() + 
                        '</div>' +
                        '<div class="card-body">' +
                            '<blockquote class="blockquote mb-0">' +
                                '<p>' + json.body + '</p>' +
                                '<footer class="blockquote-footer">' + json.name + '</footer>' +
                            '</blockquote>' +
                        '</div>' +
                    '</div>'
                )
            },
            error: function(xhr, errmsg, err){
                console.log(xhr.status + ': ' + xhr.responseText);
            }
        });
    });
});