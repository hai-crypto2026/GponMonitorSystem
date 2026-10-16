<script>location.href='../../index.php';</script><script>
    loadCSS("vendors/css/select2.min.css");
    loadCSS("vendors/css/timeline.css");
    loadCSS("vendors/plugins/datatables/media/css/dataTables.bootstrap4.min.css");
    loadCSS("vendors/plugins/datatables/extensions/Select/css/select.dataTables.min.css");
    loadCSS("vendors/plugins/datatables/extensions/Select/css/select.bootstrap.css");
    loadCSS("vendors/css/sweetalert.css");
    loadCSS("https://cdn.datatables.net/fixedcolumns/4.2.1/css/fixedColumns.dataTables.min.css");
    loadCSS("https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.css");
    var requireJS = [
        "vendors/js/select2.min.js",
        "vendors/js/bootstrap-input-spinner.js",
        "vendors/js/jquery.table2excel.min.js",
        "vendors/js/jquery.dataTables.min.js",
        "vendors/plugins/datatables/media/js/dataTables.bootstrap4.min.js",
        "vendors/plugins/datatables/extensions/Select/js/dataTables.select.min.js",
        "vendors/plugins/datatables/media/js/buttons.html5.min.js",
        "vendors/plugins/datatables/media/js/dataTables.buttons.min.js",
        "vendors/plugins/datatables/media/js/jszip.min.js",
        "vendors/js/ladda.min.js",
        "vendors/js/sweetalert.min.js",
        "https://cdn.datatables.net/fixedcolumns/4.2.1/js/dataTables.fixedColumns.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.js"
    ];

    loadJS(requireJS, "js/views/quanlyonu.js");
</script>
<div id="infohis" class="modal fade" role="dialog">
    <div class="modal-dialog modal-md" role="document">
        <div class="modal-content">
            <div class="modal-header bg-primary">
                <h4 class="modal-title">XEM THÔNG TIN LỊCH SỬ</h4>
                <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span></button>
            </div>
            <div class="modal-body">
                <div class="col-md-3" style="display: none">
                    <div class="form-group">
                        <label for="name">Mã OLT</label>
                        <div class="form-line">
                            <input type="text" id="oltid" name="oltid" class="form-control" value="now">
                        </div>
                    </div>
                </div>
                <div class="col-md-3" style="display: none">
                    <div class="form-group">
                        <label for="name">Mã ONU</label>
                        <div class="form-line">
                            <input type="text" id="onuid" name="onuid" class="form-control" value="now">
                        </div>
                    </div>
                </div>
                <div class="col-md-3" style="display: none">
                    <div class="form-group">
                        <label for="name">Type olt</label>
                        <div class="form-line">
                            <input type="text" id="type_olt" name="type_olt" class="form-control" value="now">
                        </div>
                    </div>
                </div>
                <div class="col-md-3" style="display: none">
                    <div class="form-group">
                        <label for="name">Khu vực</label>
                        <div class="form-line">
                            <input type="text" id="khuvuc_his" name="khuvuc_his" class="form-control" value="now">
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-group">
                        <label for="name">Ngày bắt đầu</label>
                        <div class="form-line">
                            <input type="date" id="ngaybatdau" name="ngaybatdau" class="form-control" value="now">
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-group">
                        <label for="name">Ngày kết thúc</label>
                        <div class="form-line">
                            <input type="date" id="ngayketthuc" name="ngayketthuc" class="form-control" value="now">
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <label>Lỗi tín hiệu (Rx <-26 dBm)</label>
                <div class="form-group">
                    <label class="switch switch-text switch-danger">
                        <input type="checkbox" class="switch-input" name="loitinhieu"id="loitinhieu">
                        <span class="switch-label" data-on="On" data-off="Off"></span>
                        <span class="switch-handle"></span>
                    </label>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-primary col-md-3" id="xnxacnhan">Xác Nhận</button>
            </div>
        </div>
    </div>
</div>
<div id = "viewupdate" class = "modal fade" role = "dialog">
    <div class = "modal-dialog modal-md" role = "document">
        <div class="modal-content">
            <div class="modal-header bg-primary">
                <h4 class="modal-title">Update Firmware ONU</h4>
                <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span></button>
            </div>
            <div class = "modal-body">
                <div class = "col-lg-12 col-md-12 col-sm-12 col-xs-12">
                    <div class="row" >
                        <div class = "form-group col-md-6">
                            <label for="name"><b>Mã ONU</b></label>
                            <div class = "form-line">
                                <input type = "text" id = "maonu" class = "form-control" value = ""readonly="true">
                            </div>
                        </div>
                        <div class = "form-group col-md-6">
                            <label for="name"><b>Model</b></label>
                            <div class = "form-line">
                                <input type = "text" id = "model" class = "form-control" value = ""readonly="true">
                            </div>
                        </div>
                    </div>
                    <div class="row" >
                        <div class = "form-group col-md-12">
                            <label for="name"><b>Firmware</b></label>
                            <select class = "form-control show-tick" name = "firmware" id = "firmware"  data-live-search = "true">
                            </select>
                        </div>
                    </div>
                    <div class="row" >
                        <div class="form-group col-md-6">
                            <label for="name"><b>Download from FTP</b></label>
                            <div class = "form-line">
                                <label class="switch switch-text switch-danger">
                                    <input type="checkbox" class="switch-input"name="ftp_check"id="ftp_check">
                                    <span class="switch-label" data-on="Yes" data-off="No"></span>
                                    <span class="switch-handle"></span>
                                </label>
                            </div>
                        </div>
                        <div class="form-group col-md-6">
                            <label for="name"><b></b></label>
                            <div class = "form-line">
                                <button type="button" class="btn btn-primary col-md-6" id="btn_xacnhan">Dowload FW</button>
                            </div>
                        </div>

                    </div>
                    <div class="row" >
                        <div class="form-group col-lg-12">
                            <label for="name"><b>Firmware Version</b></label>
                            <div class = "form-line" id="firmware_version">

                            </div>
                        </div>
                    </div>
                    <div class="row" >
                        <label for="name" class="text-red"><i>Chú ý: Sau khi download FW thành công mới được Commit Os</i></label>
                    </div>
                    <div class="row" >
                        <div class="form-group col-md-6">
                            <label for="name"><b>Chọn OS</b></label>
                            <div class="form-group col-md-6 ">
                                <div class = "form-line">
                                    <div class = "form-group ">
                                        <select class = "form-control show-tick" name = "os_check" id = "os_check"  data-live-search = "true">
                                            <option value="os1">Os1</option>
                                            <option value="os2">Os2</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="form-group col-md-6">
                            <label for="name"><b></b></label>
                            <div class = "form-line">
                                <button type="button" class="btn btn-primary col-md-6" id="btn_commit">Commit OS</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<section class="content">
    <div id="kiemtratinhieu" class="modal fade" role="dialog">
        <div class="modal-dialog modal-lg" style="overflow-y: auto;" role="document">
            <div class="modal-content">
                <div class="modal-header bg-primary">
                    <h4 class="modal-title">XEM THÔNG TIN ONU</h4>
                    <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span></button>
                </div>
                <div class="modal-body" id="ketquatelnet">;
                    Đang tiến hành lấy thông tin..
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Đóng</button>
                </div>
            </div>
        </div>
    </div>
    <div id="kiemtraS1S2" class="modal fade" role="dialog">
        <div class="modal-dialog modal-lg" style="overflow-y: auto;" role="document">
            <div class="modal-content">
                <div class="modal-header bg-primary">
                    <h4 class="modal-title">XEM THÔNG TIN ODF</h4>
                    <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span></button>
                </div>
                <div class="modal-body" id="ketquaODF">;
                    Đang tiến hành lấy thông tin..
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Đóng</button>
                </div>
            </div>
        </div>
    </div>
    <!-- Tìm kiếm -->

    <div class="row clearfix">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">

            <div class="tab-pane active show" id="dasan" role="tabpanel">
                <div class="card-header bg-dark-blue text-white">
                    <i class="fa fa-search-plus"></i><b>TÌM KIẾM</b>
                </div>
                <div class="card-body" id="divtimkiem" class="collapse">
                    <form id="timkiem" action="quanlyonu.php" method="POST">
                        <div class="row clearfix">
                            <div class="col-md-2">
                                <label>Lỗi tín hiệu (Rx <-26 dBm)</label>
                                <div class="form-group">
                                    <label class="switch switch-text switch-danger">
                                        <input type="checkbox" class="switch-input" name="loitinhieu_dasan"id="loitinhieu_dasan">
                                        <span class="switch-label" data-on="On" data-off="Off"></span>
                                        <span class="switch-handle"></span>
                                    </label>
                                </div>
                            </div>
                            <div class="col-md-2">
                                <label>Trạng thái(Active)</label>
                                <div class="form-group">
                                    <label class="switch switch-text switch-success">
                                        <input type="checkbox" class="switch-input" name="trangthai"id="trangthai">
                                        <span class="switch-label" data-on="On" data-off="Off"></span>
                                        <span class="switch-handle"></span>
                                    </label>
                                </div>
                            </div>
                            <div class="col-md-2" id="timmaonu">
                                <div class="form-group">
                                    <div class="form-line">
                                        <label>Mã ONU</label>
                                        <input type="text" class="form-control" id="maonu_1" name="maonu_1" placeholder="Nhập vào mã ONU">
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-2">
                                <div class="form-group">
                                    <div class="form-line">
                                        <label>  </label>
                                        <button type="button" class="btn btn-block bg-primary waves-effect waves-blue waves-float "id="xntimkiem" name="timkiem" ><i class="fa fa-search"></i> TRA CỨU</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
                <div class="card">
                    <div class="card-header bg-dark-blue text-white">
                        <i class="fa fa-address-book"></i><b>THỐNG KÊ THÔNG TIN ONU</b>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table style="font-size: 12px; font-family: Verdana;" width="100%" cellspacing="0" class="table table-bordered table-striped table-hover js-basic-table display nowrap" id="autoTables">
                                <thead>
                                    <tr>
                                        <th class="noExl">Công Cụ</th>
                                        <th>Mã ONU</th>
                                        <th>Trạng thái</th>
                                        <th>Rx(1490)</th>
                                        <th>Rx(1310)</th>
                                        <th>Chi nhánh</th>
                                        <th>Địa chỉ</th>
                                        <th>Mode</th>
                                        <th>Profile</th>
                                        <th>Firmware</th>
                                        <th>Deactive Reason</th>
                                        <th>Inactive Time</th>
                                        <th>Mã OLT</th>
                                        <th>Port Pon</th>
                                        <th>ONU ID</th>
                                        <th>Model</th>
                                        <th>Khoảng cách</th>
                                        <th>Thời gian</th>
                                        <th>Type OLT</th>
                                        <th>IP OLT</th>
										<th>Model Olt</th>
                                        <th>Row ID</th>
                                    </tr>
                                </thead>
                                <tfoot>
                                    <tr class="noExl">
                                        <th>Công Cụ</th>
                                        <th>Mã ONU</th>
                                        <th>Trạng thái</th>
                                        <th>Rx Power(1490)</th>
                                        <th>Rx(1310)</th>
                                        <th>Chi nhánh</th>
                                        <th>Địa chỉ</th>
                                        <th>Mode</th>
                                        <th>Profile</th>
                                        <th>Firmware</th>
                                        <th>Deactive Reason</th>
                                        <th>Inactive Time</th>
                                        <th>Mã OLT</th>
                                        <th>Port Pon</th>
                                        <th>ONU ID</th>
                                        <th>Model</th>
                                        <th>Khoảng cách</th>
                                        <th>Thời gian</th>
                                        <th>Type OLT</th>
                                        <th>IP OLT</th>
										<th>Model Olt</th>
                                        <th>Row ID</th>
                                    </tr>
                                </tfoot>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</section>
