import re

date_pattern = r"\[\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4}]"
error_request_pattern = r'"GET.*" 4\d\d'


def time_to_seconds(date_str: str):
    return int(date_str[13:15])*3600 + int(date_str[16:18])*60 + int(date_str[19:21])


def get_logs_for_period(log_file, month: str, from_time: str, to_time: str):
    result = []
    for line in log_file.readlines():
        date = re.search(date_pattern, line).group()
        if date[4:7] == month:
            if (date[1:3] == from_time[1:3]) and (time_to_seconds(from_time) <= time_to_seconds(date)):
                result.append(line)
            elif from_time[1:3] < date[1:3] < to_time[1:3]:
                result.append(line)
            elif (date[1:3] == to_time[1:3]) and (time_to_seconds(date) <= time_to_seconds(to_time)):
                result.append(line)

    return result


def main():
    with open("logs") as logs:
        period_logs = get_logs_for_period(logs, "Mar", "[22/Mar/2009:19:25:21]", "[29/Mar/2009:12:00:00]")
        final_result = []
        for line in period_logs:
            if re.search(error_request_pattern, line) is not None:
                final_result.append(line)
        with open("search_results", "w") as res:
            for line in final_result:
                print(line)
                res.write(line)


if __name__ == "__main__":
    main()
