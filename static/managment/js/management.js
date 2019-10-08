function task_name(tasktype){
    var get_id = tasktype.dataset.whatever;
    // task_nameメソッドによって、モーダル内の値を検索している。モーダル内のname属性が、「tasktype」と取得している
    const result = document.getElementById('taskname');
    result.value = get_id;
}