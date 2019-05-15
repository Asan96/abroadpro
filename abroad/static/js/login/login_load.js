let reg = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;
function alert_msg(msg){
    swal(msg, {
        button: false,
    });
}
$('#btn_login').click(function () {
    let params;
    params = {
        "user_id": $('#user_id').val(),
        "password": $('#password').val()
    };
    $.ajax({
        type : "POST",
        url : PUB_URL.dataUser,
        dataType : "json",
        data : params,
        success : function(data) {
            if (data.ret){
                location.href ='abroad/home'
            } else {
                alert_msg(data.msg)
            }
        },
        error : function (XMLHttpRequest, textStatus, errorThrown) {
            // alert(XMLHttpRequest.status+" "+textStatus+" "+errorThrown)
            alert_msg(XMLHttpRequest.status+" "+textStatus+" "+errorThrown)
        }
    });
});
$('#register_name').blur(function () {
    let register_name = $('#register_name').val();
    let len = (register_name).length;
    if (len<1 || len>8){
        $('#register_name').val('');
    }
});
$('#first_password').blur(function () {
    blur_first_password('#first_password')
});
$('#modify_first_password').blur(function () {
    blur_first_password('#modify_first_password')
});
$('#second_password').blur(function () {
    blur_second_password('#first_password','#second_password')
});
$('#modify_second_password').blur(function () {
    blur_second_password('#modify_first_password','#modify_second_password')
});
function blur_first_password(first_password){
    let len = $(first_password).val().length;
    if (len<6 || len>16){
        $(first_password).val('');
    }
}
function blur_second_password(first_password,second_password){
    let first = $(first_password).val();
    let second = $(second_password).val();
    if (first != second){
        $(second_password).val('');
    }
}
$('#register_email').blur(function () {
    let email = $('#register_email').val();
    if(!reg.test(email))
    {
        $('#register_email').val('');
        $('#register_email').attr('placeholder',"邮箱格式错误！");
    }
});
/**
 * 重置注册参数
 * */
function clear_register_params(){
    $('#register_email').attr('placeholder',"邮箱用于找回密码");
    $('#register_email').val('');
    $('#register_id').val('');
    $('#first_password').val('');
    $('#second_password').val('');
    $('#register_name').val('');
    $('#register_birth').val('');
    $('#register_sex').val('');
}
/*
* 重置找回密码参数
* */
function clear_modify_params(){
    $('#modify_user_id,#modify_email,#modify_msg,#modify_first_password,#modify_second_password').val('');
}
$('#mod_register').on('hide.bs.modal', function () {
    clear_register_params();
});
$('#mod_modify_password').on('hide.bs.modal', function () {
    clear_modify_params();
});
/*
* 注册信息校验
* */
$('#href_register').click(function () {
    $('#mod_register').modal('show');
    $('#btn_submit').unbind().click(function () {
        let params ={
            "user_id": $('#register_id').val(),
            "first_password" : $('#first_password').val(),
            "second_password": $('#second_password').val(),
            "user_name": $('#register_name').val(),
            "birthday": $('#register_birth').val(),
            "sex": $('#register_sex').val(),
            "email": $('#register_email').val(),
        };
        if (params['user_id']===''||params['user_id'].length<2||params['user_id'].length>8)
        {
            $('#register_id').val('');
            alert_msg('请按提示填写账号！')
        }else if (params['first_password'] === '' ||params['second_password']==='')
        {
            alert_msg('请按提示填写密码！')
        }else if (params['user_name'] === ''||params['user_name'].length<2||params['user_name'].length>8)
        {
            alert_msg('请按提示填写昵称！')
        }else if (params['email'] === ''){
            alert_msg('请填写邮箱，以便忘记密码后找回！')
        } else{
            $.ajax({
                type : "POST",
                url : PUB_URL.dataRegister,
                dataType : "json",
                data : params,
                success : function(data) {
                    if (data.ret){
                        alert_msg(data.msg)
                    } else {
                        alert_msg(data.msg)
                    }
                    $('#mod_register').modal('hide');
                },
                error : function (XMLHttpRequest, textStatus, errorThrown) {
                    alert_msg(XMLHttpRequest.status+" "+textStatus+" "+errorThrown)
                }
            })
        }

    });
});
/*
* 修改密码
* */
$('#href_modify_password').click(function () {
    $('#mod_modify_password').modal('show');
});
/**
 * 邮箱验证码发送
 * */
$('#btn_verify').click(function () {
    let params = {
        'email': $('#modify_email').val(),
        'user_id': $('#modify_user_id').val(),
    };
    if (params['user_id'] == '')
    {
        alert_msg('请输入要找回密码的账号!')
    }
    else if (params['email'] ==''){
        alert_msg('请输入邮箱地址!')
    }else if (!reg.test(params['email']))
    {
        alert_msg('请输入正确格式的邮箱地址!')
    }else{
        $.ajax({
                type : "POST",
                url : PUB_URL.dataSendVerify,
                dataType : "json",
                data : params,
                success : function(data) {
                    if (data.ret){
                        alert_msg(data.msg)
                    } else {
                        alert_msg(data.msg)
                    }
                },
                error : function (XMLHttpRequest, textStatus, errorThrown) {
                    // alert(XMLHttpRequest.status+" "+textStatus+" "+errorThrown)
                    alert_msg(XMLHttpRequest.status+" "+textStatus+" "+errorThrown)
                }
            })
    }
});
/*
* 验证码校验提示
* */
$('#modify_msg').blur(function () {
    let params = {
        'email': $('#modify_email').val(),
        'user_id': $('#modify_user_id').val(),
        'verify_msg' : $('#modify_msg').val(),
    };
    if (params['email']!=='' &&params['user_id']!==''&&params['verify_msg']!==''){
        $.ajax({
                type : "POST",
                url : PUB_URL.dataCheckVerify,
                dataType : "json",
                data : params,
                success : function(data) {
                    if (data.ret){
                        alert_msg(data.msg)
                    } else {
                        $('#modify_msg').val('');
                        alert_msg(data.msg)
                    }
                },
                error : function (XMLHttpRequest, textStatus, errorThrown) {
                    // alert(XMLHttpRequest.status+" "+textStatus+" "+errorThrown)
                    alert_msg(XMLHttpRequest.status+" "+textStatus+" "+errorThrown)
                }
            })
    }
});
/*
* 修改新密码
* */
$('#btn_modify_password').click(function () {
    let JudgeNum = 1;
    $("#mod_modify_password").find("input[type='text']").each(function () {
        if ($(this).val() == "") {
            JudgeNum = 0;
        }
    });
    $("#mod_modify_password").find("input[type='password']").each(function () {
        if ($(this).val() == "") {
            JudgeNum = 0;
        }
    });
    if (JudgeNum ===0) {
        alert_msg('请将信息填写完整!')
    }
    else{
        let params = {
        'email': $('#modify_email').val(),
        'user_id': $('#modify_user_id').val(),
        'verify_msg' : $('#modify_msg').val(),
        'password' : $('#modify_second_password').val(),
        };
        $.ajax({
            type : "POST",
            url : PUB_URL.dataModifyPassword,
            dataType : "json",
            data : params,
            success : function(data) {
                if (data.ret){
                    alert_msg(data.msg)
                    $('#mod_modify_password').modal('hide');
                } else {
                    $('#modify_msg').val('');
                    alert_msg(data.msg)
                }
            },
            error : function (XMLHttpRequest, textStatus, errorThrown) {
                // alert(XMLHttpRequest.status+" "+textStatus+" "+errorThrown)
                alert_msg(XMLHttpRequest.status+" "+textStatus+" "+errorThrown)
            }
        })
    }
});
