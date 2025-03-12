import * as React from 'react';
import { DemoContainer, DemoItem } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';

// const datePickerLabel = 'Select the date (ET)'

export default function ResponsivePickers({ date, onChange, minDate, maxDate, label }) {
    return (
        <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DemoContainer components={['DatePicker']}>
                <DemoItem label={label}>
                    <DatePicker
                        defaultValue={date}
                        onChange={onChange}
                        minDate={minDate}
                        maxDate={maxDate}
                    />
                </DemoItem>
            </DemoContainer>
        </LocalizationProvider>
    );
}