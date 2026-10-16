<!DOCTYPE html>
<html>

<head>
    <meta http-equiv="X-Frame-Options" content="deny">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Hệ thống quản trị Phòng Kỹ thuật - INC</title>
    <link rel="shortcut icon" href="img/favicon/favicon.ico">
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link href="font-awesome/css/all.min.css" rel="stylesheet">
    <!-- Toastr style -->
    <link href="css/plugins/toastr/toastr.min.css" rel="stylesheet">
    <!-- Gritter -->
    <link href="js/plugins/gritter/jquery.gritter.css" rel="stylesheet">
    <link href="css/animate.css" rel="stylesheet">
    <link href="css/style.css" rel="stylesheet">
    <link href="css/plugins/sweetalert/sweetalert.css" rel="stylesheet" type="text/css" />
</head>

<body class="md-skin gray-bg">
    <div class="middle-box text-center loginscreen animated fadeInDown">
        <div class="row">
            <div class="ibox float-e-margins">
                <div class="ibox-title bg-success">
                    <h1 class="logo-name">
                        <img src="img/logovtvcab.png" class="img-responsive" style="width: 350px;" />
                    </h1>
                    <h3> PHÒNG KỸ THUẬT - INC</h3>
                    <p>Hệ thống quản trị, giám sát hạ tầng viễn thông</p>
                </div>
                <div class="ibox-content">
                    <div class="form-group">
                        <input type="text" id="username" class="form-control" placeholder="Email do VTVcab cung cấp" required="">
                    </div>
                    <div class="form-group">
                        <input type="password" id="password" class="form-control" placeholder="Mật khẩu địa chỉ email" required="">
                    </div>
                    <button type="submit" id="btn_login" class="btn dim btn-success block full-width m-b">Đăng nhập</button>
                </div>
            </div>
            <p class="m-t"> <small>Phòng Kỹ thuật - INC &copy; 2020</small> </p>
        </div>
    </div>

    <!-- Mainly scripts -->
    <script src="js/jquery-3.1.1.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/plugins/sweetalert/sweetalert.min.js" type="text/javascript"></script>
    <script type="text/javascript">
        if (top.location !== self.location) {
            top.location = self.location;
        }
        $('#btn_login').on('click', function() {
            // try {
                var username = document.getElementById('username').value;
                if (username.length === 0) {
                    swal("THÔNG BÁO", "Bạn chưa nhập vào địa chỉ email!", "warning");
                    return false;
                }
                var password = document.getElementById('password').value;
                if (password.length === 0) {
                    swal("THÔNG BÁO", "Bạn chưa nhập vào password!", "warning");
                    return false;
                }
                $.ajax({
                    type: "POST",
                    url: "api/tools/login.php",
                    data: {
                        "username": username,
                        "password": password
                    },
                    beforeSend: function() {
                        document.getElementById('btn_login').innerHTML = '<i class="fa fa-spinner fa-spin"></i> Đăng nhập';
                    },
                    success: function(obj) {
                        if (obj) {
                            switch (obj) {
                                case "TRUE":
                                    window.location.href = 'modules.php';
                                    break;
                                case "PERMISSION":
                                    swal("THÔNG BÁO", "Bạn chưa được phân quyền truy cập hệ thống!", "warning");
                                    break;
                                case "INFO":
                                    swal("THÔNG BÁO", "Thông tin đăng nhập không chính xác!", "warning");
                                    break;
                                case "ERROR":
                                    swal("THÔNG BÁO", "Lỗi hệ thống!", "warning");
                                    break;
                            }
                        } else {
                            swal("THÔNG BÁO", "Lỗi hệ thống!", "warning");
                        }
                    },
                    complete: function() {
                        document.getElementById('btn_login').innerHTML = 'Đăng nhập';
                    }
                });
            // } catch (err) {
                // swal("THÔNG BÁO", "Lỗi hệ thống!", "warning");
            // }
        });

        $("#username").keyup(function(event) {
            if (event.keyCode === 13) {
                $("#btn_login").click();
            }
        });

        $("#password").keyup(function(event) {
            if (event.keyCode === 13) {
                $("#btn_login").click();
            }
        });
    </script>
</body>

</html>