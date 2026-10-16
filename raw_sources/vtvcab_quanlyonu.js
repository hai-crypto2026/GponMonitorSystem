$(window).scroll(function () {
    if ($(this).scrollTop() >= 50) {        // If page is scrolled more than 50px
        $('#return-to-top').fadeIn(200); // Fade in the arrow
    } else {
        $('#return-to-top').fadeOut(200); // Else fade out the arrow
    }
});
$('#return-to-top').click(function () {      // When arrow is clicked
    $('body,html').animate({
        scrollTop: 0                       // Scroll to top of body
    }, 500);
});
var interval;
var table = $('#autoTables').DataTable({
});

$(function () {

    Ladda.bind('.btn-ladda');
    $("input[type='number']").inputSpinner();
    $('#firmware').select2({
        theme: "bootstrap"
    });
});

$('#xntimkiem').click(function () {

    var loitinhieu = document.getElementById('loitinhieu_dasan').value;
    loitinhieu = false;
    if ($('#loitinhieu_dasan').is(':checked')) {
        loitinhieu = $('#loitinhieu_dasan').is(':checked');
    } else {
        loitinhieu = $('#loitinhieu_dasan').is(':checked');
    }
    var trangthai = document.getElementById('trangthai').value;
    trangthai = false;
    if ($('#trangthai').is(':checked')) {
        trangthai = $('#trangthai').is(':checked');
    } else {
        trangthai = $('#trangthai').is(':checked');
    }
    var maonu = document.getElementById('maonu_1').value.trim();
    if (!maonu) {
        return  swal("Thông báo", "Nhập mã ONU cần tìm kiếm", "warning");
    }
    table.destroy();
    table = $('#autoTables').DataTable({
        ajax: {
            type: "POST",
            data: {"maonu": maonu, "loitinhieu": loitinhieu, "trangthai": trangthai, "xn": "searchOnu"},
            url: 'api/data/loaddata_onu.php',
            dataType: "json",
            complete: function () {
                swal({
                    title: 'THÔNG TIN ONU!',
                    text: 'Đang lấy thông tin...Vui lòng chờ trong giây lát !!',
                    timer: 500
                });
            }
        },
        responsive: false,
        deferRender: true,
        pagingType: "full_numbers",
//        fixedColumns: {
//            left: [2]
//        },
        lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],
        order: [[2, "asc"], [4, "asc"]],
        dom: 'Blfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Save as Excel',
                exclude: ".noExl",
                exportOptions: {
                    columns: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
                }
            }
        ],
        columnDefs: [{
                defaultContent: "-",
                targets: "_all",
                className: "text-center"
            },
            {
                targets: 0,
                data: null,
                render: function (data, type, row) {
                    return '<div class="dropdown">'
                            + '<button class="btn btn-secondary dropdown-toggle btn btn-primary" type="button" id="dropdownMenu2" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Công Cụ'
                            + '</button>'
                            + '<div class="dropdown-menu" aria-labelledby="dropdownMenu2" x-placement="bottom-start" style="position: absolute; transform: translate3d(0px, 20px, 0px); top: 0px; left: 0px; will-change: transform;">'
                            + '<button class="dropdown-item" type="button" onclick="opencheck(\'' + row["OLTIP"] + '\',\'' + row["SNONU"] + '\',\'' + row["PORTPON"] + '\',\'' + row["ONUID"] + '\',\'pppoe\',\'' + row["TYPE_OLT"] + '\',\'' + row["MODELS"] + '\');">PPPoE</button>'
                            + '<button class="dropdown-item" type="button" onclick="opencheck(\'' + row["OLTIP"] + '\',\'' + row["SNONU"] + '\',\'' + row["PORTPON"] + '\',\'' + row["ONUID"] + '\',\'real\',\'' + row["TYPE_OLT"] + '\',\'' + row["MODELS"] + '\');">Tín Hiệu</button>'
                            + '<button class="dropdown-item" type="button" onclick="update_infor_customer(\'' + row["SNONU"] + '\');">Cập nhật thông tin KH</button>'
                            + '<button class="dropdown-item" type="button" onclick="loadS1S2(\'' + row["SNONU"] + '\');">Hộp S2</button>'
                            + '<button class="dropdown-item" type="button" onclick="upgradeONU(\'' + row["OLTIP"] + '\',\'' + row["SNONU"] + '\',\'' + row["PORTPON"] + '\',\'' + row["ONUID"] + '\',\'' + row["MODEL"] + '\',\'' + row["TYPE_OLT"] + '\',\'' + row["MODELS"] + '\');">Update firmware</button>'
                            + '<button class="dropdown-item" type="button" onclick="resetONU(\'' + row["OLTIP"] + '\',\'' + row["PORTPON"] + '\',\'' + row["ONUID"] + '\',\'' + row["TYPE_OLT"] + '\',\'' + row["MODELS"] + '\');">Reset</button>'
                            + '<button class="dropdown-item" onclick="openhistory(\'' + row["SNONU"] + '\');" type="button" >Lịch Sử</button>'
                            + '</div>'
                            + '</div>';
                }
            },
            {
                targets: 2,
                data: "STATUS_NAME",
                render: function (data, type, row) {
                    if (row["STATUS_NAME"] === 'Active' || row["STATUS_NAME"] === 'Working' || row["STATUS_NAME"] === 'Enabled') {
                        return '<span class="badge badge-success">' + data + '</span>';
                    } else {
                        return '<span class="badge badge-danger">' + data + '</span>';
                    }
                }
            },

            {
                targets: 3,
                data: "RXPOWER",
                render: function (data) {
                    if (data <= -8 && data > -24) {
                        return '<span class="badge badge-success">' + data + '</span>';
                    } else if (data >= -26 && data <= -24) {
                        return '<span class="badge badge-warning">' + data + '</span>';
                    } else if (data < -26 || data > -8) {
                        return '<span class="badge badge-danger">' + data + '</span>';
                    }
                }
            },
            {
                targets: 4,
                data: "RXPOWER_1310",
                render: function (data, type, row) {
                    if (data <= -8 && data > -24) {
                        return '<span class="badge badge-success">' + data + '</span>';
                    } else if (data >= -26 && data <= -24) {
                        return '<span class="badge badge-warning">' + data + '</span>';
                    } else if (data < -26 || data > -8) {
                        return '<span class="badge badge-danger">' + data + '</span>';
                    }
                    return '-';
                }
            },
            {
                targets: 7,
                data: "MODE_NAME",
                render: function (data, type, row) {
                    return data;
                }
            },
            {
                targets: 10,
                data: "DEACTIVE_NAME",
                render: function (data, type, row) {
                    if (row["STATUS_NAME"] === 'Active' || row["STATUS_NAME"] === 'Working') {
                        return '-';
                    } else {
                        return '<span class="badge badge-danger">' + data + '</span>';
                    }

                }
            },
            {
                targets: 11,
                data: "INACTIVE_TIME",
                render: function (data, type, row) {
                    var day = Math.floor(data / 86400);
                    data -= day * (86400);
                    var hours = Math.floor(data / (3600));
                    data -= hours * 3600;
                    var munites = Math.floor(data / 60);
                    data -= munites * 60;
                    var second = Math.floor(data);
                    data -= second;
                    return  day + "d " + hours + "h " + munites + "m " + second + "s ";
                }
            },
            {
                targets: 19,
                visible: false
            },
            {
                targets: 20,
                visible: false
            },
			{
                targets: 21,
                visible: false
            },
			
        ],
        columns: [
            {data: null},
            {data: "SNONU"},
            {data: "STATUS_NAME"},
            {data: "RXPOWER"},
            {data: "RXPOWER_1310"},
            {data: "BRANCH"},
            {data: "ADDRESS"},
            {data: "MODE_NAME"},
            {data: "PROFILEREG"},
            {data: "FIRMWARE"},
            {data: "DEACTIVE_NAME"},
            {data: "INACTIVE_TIME"},
            {data: "SNOLT"},
            {data: "PORTPON"},
            {data: "ONUID"},
            {data: "MODEL"},
            {data: "DISTANCE"},
            {data: "CREATEDATE"},
            {data: "TYPE_OLT"},
            {data: "OLTIP"},
			{data: "MODELS"},
            {data: "ROW_NUM"}
        ]
    });

});

function openhistory(maonu) {
    $('#infohis').modal('show');
    $('#onuid').val(maonu);
}
$('#xnxacnhan').click(function () {
    var maonu = document.getElementById("onuid").value;
    var ngaybatdau = document.getElementById("ngaybatdau").value;
    var ngayketthuc = document.getElementById("ngayketthuc").value;
    url = "#lichsuonu.php?maonu=" + maonu + "&ngaybatdau=" + ngaybatdau + "&ngayketthuc=" + ngayketthuc;
    window.open(url, '_blank');
    $('#infohis').modal('hide');
    $.ajax({
        type: 'POST',
        data: {"noidung": 'Xem lịch sử: maonu=' + maonu + ';ngaybatdau=' + ngaybatdau + ';ngayketthuc=' + ngayketthuc},
        url: 'api/data/loaddata_themmoilichsu.php'
    });
});
function opencheck(oltIP, maonu, portpon, onuid, tientrinh, type_olt, models) {
    $('#kiemtratinhieu').modal('show');
    document.getElementById("ketquatelnet").innerHTML = "Đang tiến hành lấy thông tin..";
    $.ajax({
        type: 'POST',
        data: {"oltIP": oltIP, "maonu": maonu, "portpon": portpon, "onuid": onuid, "tientrinh": tientrinh, "type_olt": type_olt,"models":models},
        url: 'api/telnet/getTelnet.php',
        success: function (msg) {
            if (msg) {
                document.getElementById("ketquatelnet").innerHTML = msg;
            }
        }
    });
    $.ajax({
        type: 'POST',
        data: {"noidung": 'Kiểm tra tín hiệu: Mã OLT=' + oltIP + ';Mã ONU=' + maonu + ';PortPon=' + portpon + ';ONUID=' + onuid + ';Thông tin:' + tientrinh},
        url: 'api/data/loaddata_themmoilichsu.php'
    });
}
function viewcustomer(snonu) {
    $('#kiemtratinhieu').modal('show');
    document.getElementById("ketquatelnet").innerHTML = "Đang tiến hành lấy thông tin..";
    $.ajax({
        type: 'POST',
        data: {"snonu": snonu},
        url: 'api/tools/layttkh.php',
        success: function (msg) {
            if (msg) {
                document.getElementById("ketquatelnet").innerHTML = msg;
            }
        }
    });
    $.ajax({
        type: 'POST',
        data: {"noidung": 'Kiểm tra thông tin khách hàng ;Mã ONU=' + snonu},
        url: 'api/data/loaddata_themmoilichsu.php'
    });
}
function loadOS(oltIP, portpon, onuid, type_olt,models) {
    $.ajax({
        type: 'POST',
        data: {"oltIP": oltIP, "portpon": portpon, "onuid": onuid, "type_olt": type_olt,"models":models},
        url: 'api/telnet/laydanhsach_firmware_os.php',
        success: function (msg) {
            if (msg) {
                document.getElementById('firmware_version').innerHTML = msg;
            }
        }
    });
}
function commitFW(oltIP, portpon, onuid, type_olt, models) {
    $.ajax({
        type: 'POST',
        data: {"oltIP": oltIP, "portpon": portpon, "onuid": onuid, "type_olt": type_olt,"models":models},
        url: 'api/telnet/telnet_commit_firmware_onu.php',
        success: function (msg) {
            if (msg) {
                console.log(msg);
            }
        }
    }
    );
}
function resetONU(oltIP, portpon, onuid, type_olt,models) {
    if (type_olt === "Huawei") {
        swal("Thông báo", "Liên hệ NOC - Tel : 024 36893689 nhánh : 2124, 2126, 2127");
        return false;
    }
    document.getElementById("ketquatelnet").innerHTML = "Đang tiến hành lấy thông tin..";
    swal({
        title: "Reset ONU",
        text: "Bạn có chắc chắn Reset thiết bị này không ?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#e33b0f",
        confirmButtonText: "Xác nhận!",
        cancelButtonText: "Bỏ qua",
        closeOnConfirm: false,
        showLoaderOnConfirm: true
    }, function () {
        $.ajax({
            type: 'POST',
            data: {"oltIP": oltIP, "portpon": portpon, "onuid": onuid, "type_olt": type_olt,"models":models, "xn":"reset"},
            url: 'api/telnet/telnet_reset_onu.php',
            success: function (msg) {
                if (msg !== 'FALSE') {
                    swal("THÔNG BÁO!", "Reset ONU thành công !", "success");
                } else {
                    swal("Thông Báo", 'Reset ONU thành công thất bại ', "warning");
                }
            }
        });
    });
}
function loadFW(type_fw, oltid) {
    $.ajax({
        type: 'POST',
        data: {"type_fw": type_fw, "oltid": oltid, "xn": "loadListFW"},
        url: 'api/tools/getDataUnit.php',
        success: function (msg) {
            if (msg) {
                $('select[name=firmware]').empty();
                var obj = JSON.parse(msg);
                for (var i = 0; i < obj.length; i++) {
                    $('select[name=firmware]').append('<option value="' + obj[i].NAME_FIRMWARE + '">' + obj[i].NAME_FIRMWARE + '</option>');
                }
                $('select[name=firmware]').change();
            }
        }
    });

}
function upgradeONU(oltIP, maonu, portpon, onuid, model, type_olt,models) {
    if (type_olt !== "Dasan") {
        swal("Thông báo", "Liên hệ NOC - Tel : 024 36893689 nhánh : 2124, 2126, 2127");
        return false;
    }
    loadFW(model, oltIP);
    loadOS(oltIP, portpon, onuid, type_olt, models);
    $('#viewupdate').modal('show');
    document.getElementById('maonu').value = maonu;
    document.getElementById('model').value = model;
    document.getElementById("ketquatelnet").innerHTML = "Đang tiến hành lấy thông tin..";
    $('#btn_xacnhan').click(function () {
        var name_firmware = document.getElementById('firmware').value;
        var ftp_check = document.getElementById('ftp_check').value;
        ftp_check = false;
        if ($('#ftp_check').is(':checked')) {
            ftp_check = $('#ftp_check').is(':checked');
        } else {
            ftp_check = $('#ftp_check').is(':checked');
        }
        var os_check = document.getElementById('os_check').value;
        swal({
            title: "Cập nhật FirmWare cho ONU",
            text: "Bạn có chắc chắn cập nhật Firmware này không ?",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#e33b0f",
            confirmButtonText: "Xác nhận!",
            cancelButtonText: "Bỏ qua",
            closeOnConfirm: false,
            showLoaderOnConfirm: true
        }, function () {
            $.ajax({
                type: 'POST',
                data: {"oltIP": oltIP, "portpon": portpon, "onuid": onuid, "name": name_firmware, "os_check": os_check, "xn": ftp_check, "type_olt": type_olt, "models":models},
                url: 'api/telnet/telnet_update_firmware_onu.php',
                success: function (msg) {
                    console.log(msg);
                    if (msg !== 'FALSE') {
                        swal("THÔNG BÁO!", "Đang Update Firmware... vui lòng chờ trong giây lát!", "success");
                        interval = setInterval(function () {
                            $.ajax({
                                type: 'POST',
                                data: {"oltIP": oltIP, "portpon": portpon, "onuid": onuid, "type_olt": type_olt},
                                url: 'api/telnet/laydanhsach_firmware_os.php',
                                success: function (msg) {
                                    if (msg) {
                                        document.getElementById('firmware_version').innerHTML = msg;
                                    }
                                }
                            });
                        }, 15000);
                    } else {
                        swal("Thông Báo", 'Update Firmware thất bại ', "warning");
                    }
                }
            }
            );
        });
    });
    $('#btn_commit').click(function () {
        var ftp_check = document.getElementById('ftp_check').value;
        ftp_check = false;
        if ($('#ftp_check').is(':checked')) {
            ftp_check = $('#ftp_check').is(':checked');
        } else {
            ftp_check = $('#ftp_check').is(':checked');
        }
        var os_check = document.getElementById('os_check').value;
        swal({
            title: "Commit OS",
            text: "Bạn có chắc chắn Commit OS này không ?",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#e33b0f",
            confirmButtonText: "Xác nhận!",
            cancelButtonText: "Bỏ qua",
            closeOnConfirm: false,
            showLoaderOnConfirm: true
        }, function () {
            $.ajax({
                type: 'POST',
                data: {"oltIP": oltIP, "portpon": portpon, "onuid": onuid, "os_check": os_check, "xn": ftp_check, "type_olt": type_olt,"models":models},
                url: 'api/telnet/telnet_commit_firmware_onu.php',
                success: function (msg) {
                    console.log(msg);
                    if (msg !== "FALSE") {
                        swal("THÔNG BÁO!", "Commit OS thành công !", "success");
                        interval = setInterval(function () {
                            $.ajax({
                                type: 'POST',
                                data: {"oltIP": oltIP, "portpon": portpon, "onuid": onuid, "type_olt": type_olt,"models":models},
                                url: 'api/telnet/laydanhsach_firmware_os.php',
                                success: function (msg) {
                                    if (msg) {
                                        document.getElementById('firmware_version').innerHTML = msg;
                                    }
                                }
                            });
                        }, 15000);
                    } else {
                        swal("Thông Báo", 'Commit OS thành công thất bại ', "warning");
                    }
                }
            });
        });
    });
    $('.close').click(function () {
        console.log('Close Modal');
        clearInterval(interval);
    });
    $('.modal').on('hide.bs.modal', function (e) {
        // enable your handler
        clearInterval(interval);
    });
}
function loadS1S2(maonu) {
    $('#kiemtraS1S2').modal('show');
    document.getElementById("ketquaODF").innerHTML = "Đang tiến hành lấy thông tin..";
    $.ajax({
        type: 'POST',
        data: {"snonu": maonu,"xn":"getODF"},
        url: 'api/tools/getDataUnit.php',
        success: function (msg) {
            console.log(msg);
            if (msg) {
                document.getElementById("ketquaODF").innerHTML = msg;
            }
        }
    });
}
function update_infor_customer(snonu) {
    $.ajax({
        type: 'POST',
        data: { "snonu": snonu, "xn": "updateCustomerInfo" },
        url: 'api/tools/getDataUnit.php',
        success: function (msg) {
            if (msg) {
                if (msg === "TRUE") {

                    toastr["success"]("Cập nhật thông tin khách hàng thành công!");
                }
                else {
                    toastr["error"]("Cập nhật thất bại !");
                    console.log(msg);
                }
            }
        }
    }
    );
}