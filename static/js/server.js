var app = angular.module('myApp', []);
app.controller('siteCtrl', function ($scope, $http) {
    $scope.ip_link = '127.0.0.1';
    $scope.api_link = '127.0.0.1';
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
    $scope.which = 'ip';
    $scope.search_info = '';
    $scope.url_post_data = '';
    $scope.readonly = true;
    $scope.temp = $scope.search_info == '' ? '' : '&' + $scope.which + '=' + $scope.search_info;
    $scope.selectedValue = $scope.options[0];
    if ($scope.index_html == '服务器信息页面') {
        $scope.api = 'server';
    } else if ($scope.index_html == '网络设备信息页面') {
        $scope.api = 'network';
    } else if ($scope.index_html == '数据库信息页面') {
        $scope.api = 'sql';
    } else if ($scope.index_html == '用户信息页面') {
        $scope.api = 'user';
    } else if ($scope.index_html == '广告招租') {
        $scope.api = 'user';
    }else if ($scope.index_html == '业务系统信息页面') {
        $scope.api = 'system';
    }
    $scope.url_get_data = 'http://' + $scope.api_link + '/api/' + $scope.api + '?callback=JSON_CALLBACK&start=' + $scope.start + '&end=' + $scope.end + $scope.temp;
    $scope.get_data = function (e) {
        $http.jsonp(e).success(function (res) {
            console.log(res);
            
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
    console.log($scope.url_get_data);
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
        $scope.LogOut = "http://127.0.01/logout/check";
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
            $scope.url_post_data = 'http://127.0.0.1/post/change/' + $scope.api + '?callback=JSON_CALLBACK';
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
            $scope.url_post_data = 'http://127.0.0.1/post/del/' + $scope.api + '?callback=JSON_CALLBACK';
            $scope.data_json = {
                "ID": $scope.temp_arr
            };
        } else if (e == 'add') {
            $scope.url_post_data = 'http://127.0.0.1/post/add/' + $scope.api + '?callback=JSON_CALLBACK';
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
    };
    $scope.search_input = function (e) {
        $scope.temp = $scope.search_info == '' ? '' : '&' + $scope.which + '=' + $scope.search_info;
        $scope.url_get_data = 'http://' + $scope.api_link + '/api/' + $scope.api + '?callback=JSON_CALLBACK&start=' + $scope.start + '&end=' + $scope.end + $scope.temp;
        var keycode = window.event ? e.keyCode : e.which;
        if (keycode == 13) {
            $scope.get_data($scope.url_get_data);
        }
    };
});