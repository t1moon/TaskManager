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
});

