function lookup(){
    let username=document.getElementById('username').value;
    let url='http://127.0.0.1:3000/api/member?username='+username
    fetch(url).then(
        response=>{
            return response.json();
        })
        .then(data=>{
            if(data['"data"'] == null){
                let result='查無此帳號'
                console.log(result);
                let memberName=document.getElementById('memberName');
                memberName.innerHTML=result
            }else{
                let name=data['"data"']['"name"'];
                let username=data['"data"']['"username"'];
                let result=name+'('+username+')'
                console.log(result);
                let memberName=document.getElementById('memberName');
                memberName.innerHTML=result
            }
        })
        .catch(error=>{
            console.log(error,'發生錯誤');
        });
    }

function update(){
    let url='api/member'
    let newName = document.getElementById('rename').value;
    console.log(newName);
    let config = {
        method:"PATCH",
        body:JSON.stringify({
            "name":newName
        }),
        headers:{
            "Content-Type":"application/json"
        }
    }
    fetch (url, config)
    .then(response=>{
        return response.json()
    })
    .then(data => {
        let updateStatus=document.getElementById('updateStatus');
        if(data['"ok"'] === true){
            updateStatus.innerHTML = '更新成功';
        }else{
            updateStatus.innerHTML = '更新失敗'
        }
        console.log(data);
    })
    .catch(error=>{
        console.log(error,'發生錯誤');
    });
}