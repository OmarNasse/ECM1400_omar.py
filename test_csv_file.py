from covid_data_handler import parse_csv_data, process_covid_csv_data
def test_parse_csv_data ():
    data = parse_csv_data ('nation_2021-10-28.csv')
    assert len(data) == 639

f r o m covid_data_handler i m p o r t process_covid_csv_data
d e f test_process_covid_csv_data ():
last7days_cases , current_hospital_cases , total_deaths =
process_covid_csv_data ( parse_csv_data ( ’ nation_2021 -10 -28. csv ’ ) )
assert last7days_cases == 240_299
assert current_hospital_cases == 7_019
assert total_deaths == 141_544
