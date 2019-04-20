var app = angular.module('myApp', []);
app.controller('siteCtrl', function ($scope, $http) {
    $scope.ip_link = '127.0.0.1';
    $scope.api_link = $scope.ip_link;
    $scope.start = 0;
    $scope.end = 10;
    $scope.sreach_value = ['IP', '应用', '位置'];
    $scope.change_data = 'change';
    $scope.add_data = 'add';
    $scope.del_data = 'del';
    $scope.what_crtl = '';
    $scope.index_html = document.getElementById('title').innerHTML;
    $scope.api = '';
    $scope.options = ['IP', '应用', '位置'];
    $scope.download_files = ['文件'];
    $scope.user_manage = ['账号', '权限', '用户'];
    $scope.search_info = '';
    $scope.url_post_data = '';
    $scope.readonly = true;
    $scope.temp = $scope.search_info == '' ? '' : '&' + $scope.which + '=' + $scope.search_info;
    $scope.selectedValue = $scope.options[0];
    $scope.selectedValue1 = $scope.download_files[0];
    $scope.selectedValue2 = $scope.user_manage[0];
    if ($scope.index_html == '服务器信息页面') {
        $scope.api = 'server';
    } else if ($scope.index_html == '网络设备信息页面') {
        $scope.api = 'network';
    } else if ($scope.index_html == '数据库信息页面') {
        $scope.api = 'sql';
    } else if ($scope.index_html == '用户信息页面') {
        $scope.api = 'user';
    } else if ($scope.index_html == '广告招租') {
        $scope.api = 'index';
    } else if ($scope.index_html == '业务系统信息页面') {
        $scope.api = 'system';
    }
    else if ($scope.index_html == '文件信息页面') {
        $scope.api = 'upload';
    }
    $scope.which = $scope.api == 'server' || $scope.api == 'network' || $scope.api == 'sql' || $scope.api == 'system' ? 'ip' : $scope.api == 'user' ? 'username' : $scope.api == 'upload' ? 'SFN' : '';
    $scope.url_get_data = 'http://' + $scope.api_link + '/api/' + $scope.api + '?callback=JSON_CALLBACK&start=' + $scope.start + '&end=' + $scope.end + $scope.temp;
    $scope.get_data = function (e) {
        $http.jsonp(e).success(function (res) {
            $scope.txt = res.data;
            $scope.len = res.len;
            $scope.personal_img = res.personal_img;
            $scope.call_me = res.login_user;
            $scope.new_call_me = res.login_user;
            $scope._level = res.level == 'admin' ? true : false;
            $scope.total_page = (res.len % 10) == 0 ? parseInt(res.len / 10) : parseInt(res.len / 10) + 1;
            $scope.page = $scope.range($scope.total_page);
        });
    };
    $scope.focus = 0;
    $scope.page_index = 0;
    $scope.range = function (n) {
        var arr = [];
        for (var i = 0; i < n; i++) {
            arr.push(i);
        }
        return arr;
    };
    $scope.page_index = 0;
    $scope.next_btn = function () {
        if ($scope.end < $scope.len) {
            $scope.focus++;
            if ($scope.focus > 4) {
                $scope.focus = 0;
                $scope.page_index = $scope.page_index + 5;
            }
            $scope.start = $scope.start + 10;
            $scope.end = $scope.end + 10;
            $scope.url_get_data = 'http://' + $scope.api_link + '/api/' + $scope.api + '?callback=JSON_CALLBACK&start=' + $scope.start + '&end=' + $scope.end + $scope.temp;
            $scope.get_data($scope.url_get_data);
        }
    };
    $scope.index_page_btn = function (i) {
        if (i > 4) {
            $scope.focus = 0;
            $scope.start = $scope.start + 10;
            $scope.end = $scope.end + 10;
        }
        if (i < 5 && i > -1) {
            $scope.focus = i;
            $scope.start = ($scope.page_index + i) * 10;
            $scope.end = ($scope.page_index + i + 1) * 10;
        }
        $scope.url_get_data = 'http://' + $scope.api_link + '/api/' + $scope.api + '?callback=JSON_CALLBACK&start=' + $scope.start + '&end=' + $scope.end + $scope.temp;
        $scope.get_data($scope.url_get_data);

    };
    $scope.prev_btn = function () {
        if ($scope.start > 0) {
            if ($scope.focus > 0) {
                $scope.focus--;
            } else {
                $scope.focus = 4;
                $scope.page_index = $scope.page_index - 5;
            }
            $scope.start = $scope.start - 10;
            $scope.end = $scope.end - 10;
            $scope.url_get_data = 'http://' + $scope.api_link + '/api/' + $scope.api + '?callback=JSON_CALLBACK&start=' + $scope.start + '&end=' + $scope.end + $scope.temp;
            $scope.get_data($scope.url_get_data);
        }
    };
    if ($scope.api != '') {
        $scope.get_data($scope.url_get_data);
    }
    $scope.logout = function () {
        $scope.LogOut = "http://" + $scope.ip_link + "/logout/check";
        $http.get($scope.LogOut).success(function (res) {
            window.location.reload();
        });
    };
    $scope.temp_arr = [];
    $scope.select_id = function (i) {
        $scope._tr = document.getElementsByTagName("tr");
        $scope.tmp_input = angular.element($scope._tr).eq(i + 1).find("td").eq(1).find("input").eq(0).attr("checked");
        $scope.tmp = angular.element($scope._tr).eq(i + 1).eq(0).find("td").eq(0).html();
        if ($scope.tmp_input == "checked") {
            angular.element($scope._tr).eq(i + 1).find("td").eq(1).find("input").eq(0).removeAttr("checked", "");
            $scope.temp_arr.splice($.inArray($scope.tmp, $scope.temp_arr), 1);
        }
        if ($scope.tmp_input == undefined) {
            angular.element($scope._tr).eq(i + 1).find("td").eq(1).find("input").eq(0).attr("checked", "true");
            $scope.temp_arr.push($scope.tmp);
        }
    };

    $scope.edit = function (i, a, b) {
        $scope.ID = i.ID != ('' && undefined) ? i.ID : null;
        $scope.location = i.location != ('' && undefined) ? i.location : null;
        $scope.projects = i.projects != ('' && undefined) ? i.projects : null;
        $scope.ip = i.ip != ('' && undefined) ? i.ip : null;
        $scope.login_name = i.login_name != ('' && undefined) ? i.login_name : null;
        $scope.login_password = i.login_password != ('' && undefined) ? i.login_password : null;
        $scope.remark = i.remark != ('' && undefined) ? i.remark : null;
        $scope.software = i.software != ('' && undefined) ? i.software : null;
        $scope.os = i.os != ('' && undefined) ? i.os : null;
        $scope.name = i.name != ('' && undefined) ? i.name : null;
        $scope.level = i.level != ('' && undefined) ? i.level : null;
        $scope.username = i.username != ('' && undefined) ? i.username : null;
        $scope.password = i.password != ('' && undefined) ? i.password : null;
        $scope.databases = i.databases != ('' && undefined) ? i.databases : null;
        $scope.model = i.model != ('' && undefined) ? i.model : null;
        if (a) {
            $scope.readonly = false;
        }
        $scope.what_crtl = b;
    };

    $scope.post_data = function (e) {
        $scope.data_json = {};
        if (e == 'change') {
            $scope.url_post_data = 'http://' + $scope.ip_link + '/post/change/' + $scope.api + '?callback=JSON_CALLBACK';
            $scope.data_json = {
                "ID": $scope.ID,
                "location": $scope.location,
                "projects": $scope.projects,
                "ip": $scope.ip,
                "login_name": $scope.login_name,
                "login_password": $scope.login_password,
                "remark": $scope.remark,
                "software": $scope.software,
                "name": $scope.name,
                "level": $scope.level,
                "username": $scope.username,
                "password": $scope.password,
                "databases": $scope.databases,
                "personal_img": $scope.img,
                "model": $scope.model
            };
        } else if (e == 'del') {
            $scope.url_post_data = 'http://' + $scope.ip_link + '/post/del/' + $scope.api + '?callback=JSON_CALLBACK';
            $scope.data_json = {
                "ID": $scope.temp_arr
            };
        } else if (e == 'add') {
            $scope.url_post_data = 'http://' + $scope.ip_link + '/post/add/' + $scope.api + '?callback=JSON_CALLBACK';
            $scope.data_json = {
                "ID": $scope.ID,
                "location": $scope.location,
                "projects": $scope.projects,
                "ip": $scope.ip,
                "login_name": $scope.login_name,
                "login_password": $scope.login_password,
                "remark": $scope.remark,
                "software": $scope.software,
                "name": $scope.name,
                "level": $scope.level,
                "username": $scope.username,
                "password": $scope.password,
                "databases": $scope.databases,
                "personal_img": $scope.img,
                "model": $scope.model
            };
        }
        $http.post($scope.url_post_data, $scope.data_json).success(function (res) {
            if (res == "done") {
                $scope.get_data($scope.url_get_data);
            }
        });
    };

    $scope.clean_data = function (a, b) {
        $scope.what_crtl = a;
        $scope.ID = '';
        $scope.location = '';
        $scope.projects = '';
        $scope.ip = '';
        $scope.login_name = '';
        $scope.login_password = '';
        $scope.remark = '';
        $scope.software = '';
        $scope.os = '';
        $scope.name = '';
        $scope.level = '';
        $scope.username = '';
        $scope.password = '';
        $scope.model = '';
        if (b) {
            $scope.readonly = false;
        }
    };

    function readFile() {
        var file = this.files[0];
        if (!/image|png\/\w+/.test(file.type)) {
            alert("请确保文件为图像类型");
            return false;
        }
        if (file.size > 1024 * 1024) {
            alert("头像图片大少不能超过1MB");
            return false;
        }
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function (e) {
            $scope.img = this.result;
        };
    }
    $scope.btn1 = function () {
        var input = document.getElementById("demo_input");
        if (typeof (FileReader) === 'undefined') {
            result.innerHTML = "抱歉你的浏览器不支持文件读取技术,请使用现代浏览器操作!";
            input.setAttribute('disabled', 'disabled');
        } else {
            input.addEventListener('change', readFile, false);
        }
    };

    $scope.selectedChange = function (v) {
        if (v == '位置') {
            $scope.which = 'location';
        }
        if (v == 'IP') {
            $scope.which = 'ip';
        }
        if (v == '应用') {
            $scope.which = 'projects';
        }
        if (v == '文件') {
            $scope.which = 'SFN';
        }
        if (v == '账号') {
            $scope.which = 'username';
        }
        if (v == '用户') {
            $scope.which = 'name';
        }
        if (v == '权限') {
            $scope.which = 'level';
        }
    };
    $scope.search_input = function (e) {
        $scope.temp = $scope.search_info == '' ? '' : '&' + $scope.which + '=' + $scope.search_info;
        $scope.url_get_data = 'http://' + $scope.api_link + '/api/' + $scope.api + '?callback=JSON_CALLBACK&start=' + $scope.start + '&end=' + $scope.end + $scope.temp;
        var keycode = window.event ? e.keyCode : e.which;
        if (keycode == 13) {
            $scope.get_data($scope.url_get_data);
        }
    };
    function parseFormatNum(number, n) {
        if (n != 0) {
            n = (n > 0 && n <= 20) ? n : 2;
        }
        number = parseFloat((number + "").replace(/[^\d\.-]/g, "")).toFixed(n) + "";
        var sub_val = number.split(".")[0].split("").reverse();
        var sub_xs = number.split(".")[1];
        var show_html = "";
        for (i = 0; i < sub_val.length; i++) {
            show_html += sub_val[i] + ((i + 1) % 3 == 0 && (i + 1) != sub_val.length ? "," : "");
        }
        if (n == 0) {
            return show_html.split("").reverse().join("");
        } else {
            return show_html.split("").reverse().join("") + "." + sub_xs;
        }
    }
    $scope.clean_post_data= function () {  
        $('#file1').val('');
        $('#progress').html('');
        $('#progress').css('width', "0%");
        $("#info").html('');
    };

    $(':file').change(function () {
        $('#progress').html('');
        $('#progress').css('width', "0%");
        var file = this.files[0];
        var _name = file ? file.name.split('.') : '';
        var name = file ? _name[0] : '未知';
        var size = file ? parseFormatNum(file.size / 1024 / 1024, 2) + 'MB' : '未知';
        var type = _name.length > 1 ? _name[1] : '未知';
        if (file) {
            $("#info").html("文件名：" + name + "<br>文件类型：" + type + "<br>文件大小：" + size);
        } else {
            $("#info").html('');
        }
    });

    $scope.upload = function () {
        if ($('#file1').val()) {
            var formData = new FormData($('form')[0]);
            var link="http://127.0.0.1/upload/file";
            formData.append("property", "value");
            $.ajax({
                url: link,
                type: "POST",
                data: formData,
                xhr: function () {
                    myXhr = $.ajaxSettings.xhr();
                    if (myXhr.upload) {
                        myXhr.upload.addEventListener('progress', progressHandlingFunction, false);
                    }
                    return myXhr;
                },
                success: function (result) {
                    setTimeout(function () {
                        if (result == 'done') {
                            alert('上传成功');
                            $scope.get_data($scope.url_get_data);
                        } else {
                            alert('上传类型有误');
                        }
                    }, 1000);
                },
                contentType: false,
                processData: false
            });
        }
    };

    function progressHandlingFunction(e) {
        if (e.lengthComputable) {
            $('#progress').attr({
                value: e.loaded,
                max: e.total
            });
            var percent = e.loaded / e.total * 100;
            $('#progress').html(percent.toFixed(0) + "%");
            $('#progress').css('width', percent.toFixed(0) + "%");
        }
    }
});