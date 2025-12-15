import streamlit as st

from services.baocao_service import bao_cao_doanh_thu_theo_nam


st.header("Báo cáo doanh thu theo năm")

nam = st.number_input("Năm", min_value=2000, step=1, format="%d")

if nam:
	df = bao_cao_doanh_thu_theo_nam(int(nam))

	if df.empty:
		st.info("Không có dữ liệu cho năm này.")
	else:
		st.dataframe(df, hide_index=True)

		chart_data = df.copy()
		chart_data["Tháng"] = chart_data["THANG"].apply(lambda x: f"Tháng {int(x)}")
		st.bar_chart(chart_data.set_index("Tháng")["DOANHTHU"], height=400)
else:
	st.info("Nhập năm để xem báo cáo.")
# dynamic list triệu chứng, thuốc...
# submit → gọi service
