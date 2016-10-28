/**
 * Created by timur on 19.10.16.
 */
$(document).ready(function(){
    $(".show_task_modal_title").click(function(){
        $(".show_task_modal").modal('show');
        var taskid;
        taskid = $(this).attr("data-taskid")
        $.get('/show_task', {task_id: taskid}, function(data){
            console.log(data)
            $('#task_title').html(data)
        })

    });
});

