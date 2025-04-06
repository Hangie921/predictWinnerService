import * as React from 'react';
import { DemoContainer, DemoItem } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';

// const datePickerLabel = 'Select the date (ET)'


export default function ResponsivePickers({ date, onChange, minDate, maxDate, label }) {
    const shouldDisabledDate = function(dateToBeChecked = {}) {
        let blockedDates = ["2025-03-28"]
        console.log('date is ', dateToBeChecked)
        console.log('date is ', typeof dateToBeChecked.format)
        console.log('date is ', dateToBeChecked.format("YYYY-MM-DD"))
        let formatted = typeof dateToBeChecked.format === 'function' ? dateToBeChecked.format("YYYY-MM-DD") : ""
        return blockedDates.includes(formatted)
    }
    return (
        <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DemoContainer components={['DatePicker']}>
                <DemoItem label={label}>
                    <DatePicker
                        defaultValue={date}
                        onChange={onChange}
                        minDate={minDate}
                        maxDate={maxDate}
                        shouldDisableDate={shouldDisabledDate}
                    />
                </DemoItem>
            </DemoContainer>
        </LocalizationProvider>
    );
}