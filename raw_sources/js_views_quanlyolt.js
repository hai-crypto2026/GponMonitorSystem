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
var table = $('#autoTables').DataTable({
});

$(function () {
    Ladda.bind('.btn-ladda');
    $("input[type='number']").inputSpinner();
    $('#khuvuc, #tentinh, #maolt').select2({
        theme: "bootstrap"
    });
    chonkhuvuc();
});
$('#xntimkiem').click(function () {
    var maolt = document.getElementById("maolt").value;
    table.destroy();
    table = $('#autoTables').DataTable({
        ajax: {
            type: "POST",
            data: {"maolt": maolt, "xn": "loadPortOlt"},
            url: 'api/data/loaddata_olt.php',
            dataType: "json",
            complete: function () {
                swal({
                    title: 'THÔNG TIN OLT!',
                    text: 'Đang lấy thông tin...Vui lòng chờ trong giây lát !!',
                    timer: 500
                });
            }
        },
        responsive: false,
        deferRender: true,
        select: false,
        pagingType: "full_numbers",
        lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],
        order: [[1, "asc"]],
        paging: true,
        dom: 'Blfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Save as Excel',
                exclude: ".noExl",
                exportOptions: {
                    columns: [1, 2, 3, 4]
                }
            }
        ],
        columnDefs: [
            {
                defaultContent: "-",
                targets: "_all"
            },
            {
                targets: 0,
                data: null,
                render: function (data, type, row) {
                    return '<div class="btn-group" role="group" aria-label="Basic example">'
                            + '<button type="button" onclick="danhsachonu(\'' + maolt + '\',\'' + row["PORTPON"] + '\');" class="btn btn-blue"><i class="fa icon-screen-desktop"></i>&nbsp; DS ONU</button>'
                            + '<button type="button" class="btn btn-success" onclick="showOLT_infor(\'' + maolt + '\',\'' + row["PORTPON"] + '\',\'' + row["TYPE_OLT"] + '\',\'' + row["MODELS"] + '\');"><i class="fa fa-bullseye"></i>&nbsp; Show Port</button>'
                            + '</div>';
                }
            },
            {
                targets: 5,
                visible: false
            },
            {
                targets: 6,
                visible: false
            }
        ],
        columns: [
            {data: null},
            {data: "PORTPON"},
            {data: "ACTONU"},
            {data: "INACTONU"},
            {data: "TOTALONU"},
            {data: "TYPE_OLT"},
            {data: "MODELS"}
        ]
    });

});


function chonkhuvuc() {
    $.ajax({
        type: 'POST',
        data: {"xn": "getProvinceOLT"},
        url: 'api/tools/getDataUnit.php',
        success: function (msg) {
            if (msg) {
                $('select[name=tentinh]').empty();
                var obj = JSON.parse(msg);
                for (var i = 0; i < obj.length; i++) {
                    $('select[name=tentinh]').append('<option value="' + obj[i].PROVINCE + '">' + obj[i].PROVINCE + '</option>');
                }
                $('select[name=tentinh]').change();
            }
        }
    });
}

function chontinh() {
    var e = document.getElementById("tentinh");
    tentinh = e.options[e.selectedIndex].value;
    $.ajax({
        type: 'POST',
        data: {"tentinh": tentinh, "xn": "getSingleOLT"},
        url: 'api/tools/getDataUnit.php',
        success: function (msg) {
            if (msg) {
                $('select[name=maolt]').empty();
                var obj = JSON.parse(msg);
                for (var i = 0; i < obj.length; i++) {
                    $('select[name=maolt]').append('<option value="' + obj[i].OLTID + '">' + obj[i].OLTID + '</option>');
                }
                $('select[name=maolt]').change();
            }
        }
    });
}

function danhsachonu(maolt, portpon) {

    setUpUrl("quanlyolt_danhsachonu.php?&maolt=" + maolt + "&portpon=" + portpon);
}
function showOLT_infor(maolt, portpon, typeolt, models) {
    setUpUrl("quanlyonlt_dsonu_port.php?&maolt=" + maolt + "&portpon=" + portpon + "&typeolt=" + typeolt + "&models=" + models);
}


