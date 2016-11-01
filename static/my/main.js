/**
 * Created by timur on 19.10.16.
 */
$(document).ready(function(){
    $(".delete-button").on( "click", function(){
        var $task = $(this).parent()
        var taskid = $(this).parent().attr('data-taskid')
        console.log(taskid)
        $.ajax({
            url: '/delete_task',
            type: 'POST',
            contentType: 'application/x-www-form-urlencoded',
	    	dataType: 'json',
            data: {task_id: taskid},
            success: function() {
                $task.remove()
                console.log("task deleted" + taskid)
			},
			error: function(xhr, status, error) {
				console.log(xhr.responseText + ' ' + status + ' ' + error);
			}

        })
    });

    $(".edit-button").on( "click", function(){
        var $task = $(this).parent()
        var taskid = $(this).parent().attr('data-taskid')
        $.ajax({
            url: '/edit_task/' + taskid,
            type: 'GET',
            contentType: 'application/x-www-form-urlencoded',
	    	dataType: 'json',
            success: function(data) {
                $("#edit_task_modal"+taskid).modal()
                $(".uk-form-new-task-name").val(data.title)
                $(".uk-form-new-task-description").val(data.description)
                $.each(data.tags, function(index, value) {
                    console.log(value)
                    $(".uk-form-new-task-tag").val($(".uk-form-new-task-tag").val() + value);
                    $(".uk-form-new-task-tag").val($(".uk-form-new-task-tag").val() + ', ')
                })
			},
			error: function(xhr, status, error) {
				console.log(xhr.responseText + ' ' + status + ' ' + error);
			}

        })
    });
});



