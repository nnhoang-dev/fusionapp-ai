from fusion.core.column_types import ColumnType
from fusion.core.column import Column
from fusion.core.sheet import Sheet
from fusion.core.app import FusionApp
from fusion.core.config import FusionAppConfig

app = FusionApp(config=FusionAppConfig(app_name="Hổ Châu Farmacy"))

# Create new sheets here
sheet = Sheet(id="medicines", name="Danh sách thuốc")
sheet.columns.append(Column(id="name", name="Tên thuốc", type=ColumnType.STRING))
sheet.columns.append(Column(id="quantity", name="Số lượng", type=ColumnType.INT))
sheet.columns.append(Column(id="price", name="Giá", type=ColumnType.FLOAT))
sheet.columns.append(Column(id="manufacturer", name="Nhà sản xuất", type=ColumnType.STRING))
sheet.columns.append(Column(id="expiry_date", name="Hạn sử dụng", type=ColumnType.DATE))
app.sheets.append(sheet)


sheet = Sheet(id="employees", name="Danh sách nhân viên")
sheet.columns.append(Column(id="name", name="Tên nhân viên", type=ColumnType.STRING))
sheet.columns.append(Column(id="position", name="Chức vụ", type=ColumnType.STRING))
sheet.columns.append(Column(id="salary", name="Lương", type=ColumnType.FLOAT))
sheet.columns.append(Column(id="start_date", name="Ngày bắt đầu", type=ColumnType.DATE))
app.sheets.append(sheet)

sheet = Sheet(id="payroll", name="Bảng lương")
sheet.columns.append(Column(id="employee_id", name="Mã nhân viên", type=ColumnType.STRING))
sheet.columns.append(Column(id="month", name="Tháng", type=ColumnType.INT))
sheet.columns.append(Column(id="year", name="Năm", type=ColumnType.INT))
sheet.columns.append(Column(id="working_days", name="Số ngày làm việc", type=ColumnType.INT))
sheet.columns.append(Column(id="bonus", name="Thưởng", type=ColumnType.FLOAT))
sheet.columns.append(Column(id="total_salary", name="Tổng lương", type=ColumnType.FLOAT))
app.sheets.append(sheet)