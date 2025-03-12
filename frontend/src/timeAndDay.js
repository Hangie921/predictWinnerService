import dayjs from "dayjs"
import utc from "dayjs/plugin/utc";
import timezone from "dayjs/plugin/timezone"


dayjs.extend(utc)
dayjs.extend(timezone)

const easternTimeZone = "America/New_York"

export {
    dayjs,
    easternTimeZone,
}