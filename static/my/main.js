/**
 * Created by timur on 19.10.16.
 */
$(document).ready(function () {

    // Delete

    $(document).on("click", ".delete-button", function () {
        var task = $(this).parent()
        var taskid = $(this).parent().attr('data-taskid')
        var sidebar = $(".blog-sidebar")
        var tag = sidebar.find($(".sidebar-module-category"))
        var status = sidebar.find($(".sidebar-module-status"))
        var tags_title = tag.find($(".tags")).find("span").not(".badge");

        var not_done_status_count = status.find($("#not_done_status_count")).find(".badge");
        var done_status_count = status.find($("#done_status_count")).find(".badge");
        var all_status_count = status.find($("#all_status_count")).find(".badge");
        var all_tags_count = tag.find("#all_tags_count").find(".badge");
        var none_tags_count = tag.find("#none_tags_count").find(".badge");

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

                    //delete counts in tags

                    if (data.tag_list.length == 0) {
                        none_tags_count.text(parseInt(none_tags_count.text() - 1))
                    } else {
                        all_tags_count.text(parseInt(all_tags_count.text()) - 1)
                    }

                    // detele counts in status

                    if (data.is_done) {
                        done_status_count.text(parseInt(done_status_count.text() - 1))
                        all_status_count.text(parseInt(all_status_count.text() - 1))
                    } else {
                        not_done_status_count.text(parseInt(not_done_status_count.text() - 1))
                        all_status_count.text(parseInt(all_status_count.text() - 1))
                    }


                    // delete pills from tags
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

        var sidebar = $(".blog-sidebar")
        var status = sidebar.find($(".sidebar-module-status"))
        var not_done_status_count = status.find($("#not_done_status_count")).find(".badge");
        var done_status_count = status.find($("#done_status_count")).find(".badge");

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

                    not_done_status_count.text(parseInt(not_done_status_count.text()) - 1)
                    done_status_count.text(parseInt(done_status_count.text()) + 1)
                } else {
                    console.log("TASK IS unDONE")
                    task_title.css('text-decoration', 'none');
                    task.fadeOut("slow")

                    not_done_status_count.text(parseInt(not_done_status_count.text()) + 1)
                    done_status_count.text(parseInt(done_status_count.text()) - 1)
                }
            },
            error: function (xhr, status, error) {
                console.log(xhr.responseText + ' ' + status + ' ' + error);
            }
        })
    })

    // Ajax status tag and sort

    $(".status, .tags, .sort").on("click", function () {
        var type = $(this).attr('class')
        //prepearing init values
        var sort = $(".blog-sidebar").find($(".sidebar-module-sort"))
        var tag = $(".blog-sidebar").find($(".sidebar-module-category"))
        var status = $(".blog-sidebar").find($(".sidebar-module-status"))
        var sort_last_active_pill = sort.find($(".active"))
        var tags_last_active_pill = tag.find($(".active"))
        var status_last_active_pill = status.find($(".active"))

        if (type == "sort") {
            var active_sort_title = $(this).text()
            var sort_active_pill = $(this).parent()

            var active_tag_title = tag.find($(".active")).find("span").not(".badge").text()
            var active_status_title = status.find($(".active")).find("span").not(".badge").text();

        }
        if (type == "tags") {
            var active_tag_title = $(this).find("span").not(".badge").text();
            var tags_active_pill = $(this).parent()

            var active_sort_title = sort.find($(".active")).find("a").text()
            var active_status_title = status.find($(".active")).find("span").not(".badge").text();
        }
        if (type == "status") {
            var active_status_title = $(this).find("span").not(".badge").text();
            var status_active_pill = $(this).parent()

            var active_sort_title = sort.find($(".active")).find("a").text()
            var active_tag_title = tag.find($(".active")).find("span").not(".badge").text();
        }

        $.ajax({
            url: '/',
            type: 'GET',
            contentType: 'application/x-www-form-urlencoded',
            dataType: 'json',
            data: {
                active_status_title: active_status_title,
                active_tag_title: active_tag_title,
                active_sort_title: active_sort_title
            },
            success: function (data) {
                $(".replace-tasks").html(data.html_response)

                if (type == "sort") {
                    sort_last_active_pill.removeClass("active")
                    sort_active_pill.addClass("active");
                }
                if (type == "tags") {
                    tags_last_active_pill.removeClass("active")
                    tags_active_pill.addClass("active");

                    // Need to change counts in status
                    var not_done_status_count = status.find($("#not_done_status_count")).find(".badge");
                    var done_status_count = status.find($("#done_status_count")).find(".badge");
                    var all_status_count = status.find($("#all_status_count")).find(".badge");

                    // all count = tag_count
                    all_status_count.text(data.all_status_count)
                    not_done_status_count.text(data.not_done_status_count)
                    // done_count = all - not_done
                    done_status_count.text(parseInt(all_status_count.text()) - parseInt(not_done_status_count.text()))
                }
                if (type == "status") {
                    status_last_active_pill.removeClass("active")
                    status_active_pill.addClass("active");
                }
            },
            error: function (xhr, status, error) {
                console.log(xhr.responseText + ' ' + status + ' ' + error);
            }
        })
    })

//    For tags that below a task
    $(document).on("click", '.blog-post-meta', function () {
        var sort = $(".blog-sidebar").find($(".sidebar-module-sort"))
        var tag = $(".blog-sidebar").find($(".sidebar-module-category"))
        var status = $(".blog-sidebar").find($(".sidebar-module-status"))
        var tags_last_active_pill = tag.find($(".active"))

        var active_tag_title = $(this).text().replace("#", "");
        var active_sort_title = sort.find($(".active")).find("a").text()
        var active_status_title = status.find($(".active")).find("span").not(".badge").text();

        // let's find tag on sidebar, that matches
        tags = tag.find($(".tags")).find("span").not(".badge");
        $.each(tags, function (index, value) {
            if ($(value).text() == active_tag_title) {
                tags_active_pill = $(value).parent().parent();
            }
        })
        $.ajax({
            url: '/',
            type: 'GET',
            contentType: 'application/x-www-form-urlencoded',
            dataType: 'json',
            data: {
                active_tag_title: active_tag_title,
                active_sort_title: active_sort_title,
                active_status_title: active_status_title
            },
            success: function (data) {
                $(".replace-tasks").html(data.html_response)
                tags_last_active_pill.removeClass("active")
                tags_active_pill.addClass("active");

                // Need to change counts in status
                    var not_done_status_count = status.find($("#not_done_status_count")).find(".badge");
                    var done_status_count = status.find($("#done_status_count")).find(".badge");
                    var all_status_count = status.find($("#all_status_count")).find(".badge");

                    // all count = tag_count
                    all_status_count.text(tags_active_pill.find($(".badge")).text())
                    not_done_status_count.text(data.not_done_status_count)
                    // done_count = all - not_done
                    done_status_count.text(parseInt(all_status_count.text()) - parseInt(not_done_status_count()))

            },
            error: function (xhr, status, error) {
                console.log(xhr.responseText + ' ' + status + ' ' + error);
            }
        })
    })

});



