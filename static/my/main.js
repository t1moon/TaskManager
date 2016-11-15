/**
 * Created by timur on 19.10.16.
 */
$(document).ready(function () {

    // Delete

    $(document).on("click", ".delete-button", function () {
        var task = $(this).parent()
        var taskid = $(this).parent().attr('data-taskid')
        var sidebar = $(".blog-sidebar")
        var category = sidebar.find($(".sidebar-module-category"))
        var tags_title = category.find($(".tags")).find("span").not(".badge");
        var all_tags_count = category.find("#all_tags").find(".badge");
        var none_tags_count = category.find("#none_tags").find(".badge");
        is_confirm = confirm("Вы действительно хотите удалить задачу?")
        if (is_confirm) {
            $.ajax({
                url: '/delete_task',
                type: 'POST',
                contentType: 'application/x-www-form-urlencoded',
                dataType: 'json',
                data: {task_id: taskid},
                success: function (data) {
                    task.remove()

                    //delete counts

                    if (data.tag_list.length == 0) {
                        none_tags_count.text(parseInt(none_tags_count.text() - 1))
                    } else {
                        all_tags_count.text(parseInt(all_tags_count.text()) - 1)
                    }

                    // delete from tags
                    $.each(tags_title, function (index, value) {
                        // if it's a searched tag and count == 1 then remove
                        if ($.inArray($(value).text(), data.tag_list) !== -1) {
                            tag_count = $(value).next().text();
                            if (parseInt(tag_count) == 1) {
                                $(value).parent().remove();
                            } else {
                                tag_count = tag_count - 1;
                                $(value).next().text(parseInt(tag_count));
                            }
                        }
                    })

                    console.log("task deleted" + taskid)
                },
                error: function (xhr, status, error) {
                    console.log(xhr.responseText + ' ' + status + ' ' + error);
                }

            })
        } else {
            // nothing
        }

    });

    //Edit text

    $(document).on("click", ".edit-button", function () {
        var sidebar = $(".blog-sidebar")
        var category = sidebar.find($(".sidebar-module-category"))
        var tags = category.find($(".tags")).find("span").not(".badge");
        var taskid = $(this).parent().attr('data-taskid')
        $(this).parent().children(".input-group").find(".blog-post-title").prop('readonly', false).focus()
        $(this).parent().children(".input-group").find(".blog-post-title").keypress(function (e) {
            if (e.which == 13) {
                $(this).prop('readonly', true)
                $(this).blur()
                var new_title = $(this).val()
                if (new_title == "") {
                    alert("Название не может быть пустое")
                    window.location.reload();
                } else {
                    $.ajax({
                        url: '/edit_task',
                        type: 'POST',
                        contentType: 'application/x-www-form-urlencoded',
                        dataType: 'json',
                        data: {task_id: taskid, new_title: new_title},
                        success: function () {
                            console.log("task edited" + taskid)
                        },
                        error: function (xhr, status, error) {
                            console.log(xhr.responseText + ' ' + status + ' ' + error);
                        }
                    })
                }
            }
        })
    })

    // On change deadline

    $(document).on("change", ".uk-form-deadline", function () {
        var taskid = $(this).parent().parent().parent().parent($(".blog-post")).attr('data-taskid')
        var new_deadline = $(this).val()
        var deadline = $(this)
        console.log(new_deadline)
        $.ajax({
            url: '/edit_task',
            type: 'POST',
            contentType: 'application/x-www-form-urlencoded',
            dataType: 'json',
            data: {task_id: taskid, new_deadline: new_deadline},
            success: function (data) {
                console.log("task edited" + taskid)
                if (data.task_is_over) {
                    deadline.css("box-shadow", "0px 0px 6px #d31919")
                } else {
                    deadline.css("box-shadow", "none")
                }

            },
            error: function (xhr, status, error) {
                console.log(xhr.responseText + ' ' + status + ' ' + error);
            }
        })
    })

    // Done

    $(document).on("click", ".done-button", function () {
        var task = $(this).parent().parent().parent()
        var task_title = $(this).parent().parent().find($(".blog-post-title"))
        var taskid = $(this).parent().parent().parent().attr('data-taskid')
        var is_done = task.attr('data-isdone')
        $.ajax({
            url: '/complete_task',
            type: 'POST',
            contentType: 'application/x-www-form-urlencoded',
            dataType: 'json',
            data: {task_id: taskid, is_done: is_done},
            success: function (data) {
                task.attr('data-isdone', data.is_done)
                if (data.is_done) {
                    console.log("TASK IS DONE")
                    task_title.css('text-decoration', 'line-through');
                    task.fadeOut("slow")
                } else {
                    console.log("TASK IS unDONE")
                    task_title.css('text-decoration', 'none');
                    task.fadeOut("slow")
                }
            },
            error: function (xhr, status, error) {
                console.log(xhr.responseText + ' ' + status + ' ' + error);
            }
        })
    })

    // Choice tag ajax
    $(".tags").on("click", function() {
        var tag_title = $(this).find("span").not(".badge").text();
        var list_item = $(this).parent()
        var category = $(".blog-sidebar").find($(".sidebar-module-category"))
        var sort = $(".blog-sidebar").find($(".sidebar-module-sort"))
        var last_active_pill = category.find($(".active"))
        var active_sort_title = sort.find($(".active")).find("a").text()
        $.ajax({
            url: '/',
            type: 'GET',
            contentType: 'application/x-www-form-urlencoded',
            dataType: 'json',
            data: {
                type: "tag",
                tag_title: tag_title,
                active_sort_title: active_sort_title
            },
            success: function (data) {
                $(".replace-tasks").html(data.html_response)
                last_active_pill.removeClass("active")
                list_item.addClass("active");
            },
            error: function (xhr, status, error) {
                console.log(xhr.responseText + ' ' + status + ' ' + error);
            }
        })
    })

    // For tag that are under tasks

    $(document).on("click", '.blog-post-meta', function() {
        var tag_title = $(this).text().replace("#", "");
        var category = $(".blog-sidebar").find($(".sidebar-module-category"))
        var sort = $(".blog-sidebar").find($(".sidebar-module-sort"))
        var active_sort_title = sort.find($(".active")).find("a").text()
        // let's find tag on sidebar, that matches
        tags = category.find($(".tags")).find("span").not(".badge");
        var list_item;
        $.each(tags, function(index, value) {
            if ($(value).text() == tag_title) {
                list_item = $(value).parent().parent();
            }
        })
        var last_active_pill = category.find($(".active"))
        $.ajax({
            url: '/',
            type: 'GET',
            contentType: 'application/x-www-form-urlencoded',
            dataType: 'json',
            data: {
                type: "tag",
                tag_title: tag_title,
                active_sort_title: active_sort_title
            },
            success: function (data) {
                $(".replace-tasks").html(data.html_response)
                last_active_pill.removeClass("active")
                list_item.addClass("active");
            },
            error: function (xhr, status, error) {
                console.log(xhr.responseText + ' ' + status + ' ' + error);
            }
        })
    })

    $(".sort").on("click", function() {
        var sort_title = $(this).text()
        var sort = $(".blog-sidebar").find($(".sidebar-module-sort"))
        var category = $(".blog-sidebar").find($(".sidebar-module-category"))
        var last_active_pill = sort.find($(".active"))
        var list_item = $(this).parent()
        var active_tag_title = category.find($(".active")).find("span").not(".badge").text()
        $.ajax({
            url: '/',
            type: 'GET',
            contentType: 'application/x-www-form-urlencoded',
            dataType: 'json',
            data: {
                type: "sort",
                sort_title: sort_title,
                active_tag_title: active_tag_title
            },
            success: function (data) {
                $(".replace-tasks").html(data.html_response)
                last_active_pill.removeClass("active")
                list_item.addClass("active");
            },
            error: function (xhr, status, error) {
                console.log(xhr.responseText + ' ' + status + ' ' + error);
            }
        })
    })



});



