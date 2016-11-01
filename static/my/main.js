/**
 * Created by timur on 19.10.16.
 */
$(document).ready(function(){
    $(".delete-button").on( "click", function(){
        $task = $(this).parent()
        taskid = $(this).parent().attr('data-taskid')
        $.ajax({
            url: '/delete_task/',
            type: 'POST',
            contentType: 'application/json',
	    	dataType: 'json',
            data: { id: taskid},
            success: function() {
                $task.remove()
                console.log("task deleted")
			},
			error: function(xhr, status, error) {
				console.log(xhr.responseText + ' ' + status + ' ' + error);
			}

        })
    });
});

