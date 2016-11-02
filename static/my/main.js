/**
 * Created by timur on 19.10.16.
 */
$(document).ready(function () {

    // Delete

    $(".delete-button").on("click", function () {
        var task = $(this).parent()
        var taskid = $(this).parent().attr('data-taskid')
        console.log(taskid)
        $.ajax({
            url: '/delete_task',
            type: 'POST',
            contentType: 'application/x-www-form-urlencoded',
            dataType: 'json',
            data: {task_id: taskid},
            success: function () {
                task.remove()
                console.log("task deleted" + taskid)
            },
            error: function (xhr, status, error) {
                console.log(xhr.responseText + ' ' + status + ' ' + error);
            }

        })
    });

//    $(".edit-button").on( "click", function(){
//        var $task = $(this).parent()
//        var taskid = $(this).parent().attr('data-taskid')
//        $.ajax({
//            url: '/edit_task/' + taskid,
//            type: 'GET',
//            contentType: 'application/x-www-form-urlencoded',
//	    	dataType: 'json',
//            success: function(data) {
//                $("#edit_task_modal"+taskid).modal()
//                $(".uk-form-new-task-name").val(data.title)
//                $(".uk-form-new-task-description").val(data.description)
//                $.each(data.tags, function(index, value) {
//                    console.log(value)
//                    $(".uk-form-new-task-tag").val($(".uk-form-new-task-tag").val() + value);
//                    $(".uk-form-new-task-tag").val($(".uk-form-new-task-tag").val() + ', ')
//                })
//			},
//			error: function(xhr, status, error) {
//				console.log(xhr.responseText + ' ' + status + ' ' + error);
//			}
//
//        })
//    });
    //


    //Edit text


    $(".edit-button").on("click", function () {
        var taskid = $(this).parent().attr('data-taskid')
        $(this).parent().children(".input-group").find(".blog-post-title").prop('readonly', false).focus()
        $(this).parent().children(".input-group").find(".blog-post-title").keypress(function (e) {
            if (e.which == 13) {
                $(this).prop('readonly', true)
                $(this).blur()
                var new_title = $(this).val()
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
        })
    })

    $(".uk-form-deadline").on("change", function () {
        var taskid = $(this).parent().parent().parent().parent($(".blog-post")).attr('data-taskid')
        var new_deadline = $(this).val()
        console.log(new_deadline)
        $.ajax({
            url: '/edit_task',
            type: 'POST',
            contentType: 'application/x-www-form-urlencoded',
            dataType: 'json',
            data: {task_id: taskid, new_deadline: new_deadline},
            success: function () {
                console.log("task edited" + taskid)
            },
            error: function (xhr, status, error) {
                console.log(xhr.responseText + ' ' + status + ' ' + error);
            }
        })
    })

    // Done
    $(".done-button").on("click", function () {
        var task = $(this).parent().parent().parent()
        var task_title = $(this).parent().parent().find($(".blog-post-title"))
        var taskid = $(this).parent().parent().parent().attr('data-taskid')
        var is_done = task.attr('data-isdone')
        $.ajax({
            url: '/edit_task',
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



//    Validation

$('.add_task_form').validate({ // initialize the plugin
    rules: {
        title: {
            required: true,
        },
        tags: {
            required: true,
        }
    }
});

})
;



