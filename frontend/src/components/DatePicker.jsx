import * as React from 'react';
import dayjs from 'dayjs';
import utc from "dayjs/plugin/utc";
import timezone from "dayjs/plugin/timezone"
import { DemoContainer, DemoItem } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';

dayjs.extend(utc)
dayjs.extend(timezone)

const easternTimeZone = "America/New_York"
const supportedMinDate = dayjs.tz('2024-01-01', easternTimeZone)
const supportedMaxDate = dayjs.tz('2025-12-31', easternTimeZone)
const datePickerLabel = 'Select the game date (ET)'

export default function ResponsivePickers({ date, onChange, minDate, maxDate }) {
    return (
        <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DemoContainer components={['DatePicker']}>
                <DemoItem label={datePickerLabel}>
                    <DatePicker
                        defaultValue={date}
                        onChange={onChange}
                        maxDate={supportedMaxDate}
                        minDate={supportedMinDate}
                    />
                </DemoItem>
            </DemoContainer>
        </LocalizationProvider>
    );
}