<script>location.href='../../index.php';</script><script>
    loadCSS("vendors/css/select2.min.css");
    loadCSS("vendors/css/timeline.css");
    loadCSS("vendors/plugins/datatables/media/css/dataTables.bootstrap4.min.css");
    loadCSS("vendors/plugins/datatables/extensions/Select/css/select.dataTables.min.css");
    loadCSS("vendors/plugins/datatables/extensions/Select/css/select.bootstrap.css");
    loadCSS("vendors/css/sweetalert.css");
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
        "vendors/js/sweetalert.min.js"
    ];
    loadJS(requireJS, "js/views/quanlyolt.js");
</script>
<a href="javascript:" id="return-to-top"><i class="fa fa-arrow-up"></i></a>
<div id="infohis" class="modal inmodal in" role="dialog"  aria-hidden="true">
    <div class="modal-dialog modal-xl" style="width: 1000px;" >
        <div class="modal-content">
            <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
                <div class="card-body">
                    <div class="table-responsive">
                        <table style="font-size: 12px;" width="100%" cellspacing="0" class="table table-bordered table-striped table-hover js-basic-table display nowrap" id="autoTablesC">
                            <thead>
                                <tr>
                                    <th class="noExl">Công Cụ</th>
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
<div class="row" id="top_main">
    <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
        <div class="card-header bg-dark-blue text-white">
            <i class="fa fa-search-plus"></i><b>TÌM KIẾM</b>
        </div>
        <div class="card-body" id="divtimkiem" class="collapse">
            <form id="timkiem" action="quanlyolt.php" method="POST">
                <div class="row clearfix">
                    <div class="col-md-3" id="timtentinh">
                        <label><b>Tên tỉnh</b></label>
                        <div class="form-group">
                            <select class="form-control show-tick" name="tentinh" id="tentinh" onchange="chontinh();" data-live-search="true" required>
                            </select>
                        </div>
                    </div>
                    <div class="col-md-2" id="timmaolt">
                        <label><b>Mã OLT</b></label>
                        <div class="form-group">
                            <select class="form-control show-tick" name="maolt" id="maolt" data-live-search="true" required>
                            </select>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <label></label>
                        <div class="col-md-6">
                            <button type="button" class="btn btn-block bg-primary waves-effect waves-blue waves-float "id="xntimkiem" name="timkiem" ><i class="fa fa-search"></i> TRA CỨU</button>
                        </div>
                    </div>
                </div>
            </form>
        </div>
        <div class="card">
            <div class="card-header bg-dark-blue text-white">
                <i class="fa fa-address-book"></i><b>THỐNG KÊ THÔNG TIN OLT</b>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table style="font-size: 12px;" width="100%" cellspacing="0" class="table table-bordered table-striped table-hover js-basic-table display nowrap" id="autoTables">
                        <thead>
                            <tr>
                                <th>Công cụ</th>
                                <th>Port Pon</th>
                                <th>Hoạt động</th>
                                <th>Không hoạt động</th>
                                <th>Tổng</th>
								<th>Type OLT</th>
                                <th>Models</th>
                            </tr>
                        </thead>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>