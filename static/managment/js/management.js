function task_name(tasktype){
    const get_id = tasktype.dataset.whatever; //big_task, miidel_taskを入れようとしている
    // task_nameメソッドによって、モーダル内の値を検索している。モーダル内のname属性が、「tasktype」と取得している
    const result = document.getElementById('taskname');
    result.value = get_id;
}


function each_task_type(tasktype){
    var get_id = tasktype.dataset.whatever;
    // task_nameメソッドによって、モーダル内の値を検索している。モーダル内のname属性が、「tasktype」と取得している
    const result = document.getElementById('change-task-name');
    result.value = get_id;
    const changeForm = document.getElementById("change-form");
    const modalForm = document.getElementById(tasktype.id);
    changeForm.action = modalForm.dataset.chnageurl
}

