from crawl_mlb import GetContent, Filter


def lambda_handler(event, context):
    return GetContent("json")


f = Filter()
if __name__ == "__main__":
    # 使用函式
    if len(sys.argv) == 2:
        print(GetContent("json", f.item, sys.argv[1]))
    else:
        print(GetContent("json", f.item, ""))
