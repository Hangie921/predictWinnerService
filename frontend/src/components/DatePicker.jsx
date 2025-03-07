import * as React from 'react';
import dayjs from 'dayjs';
import { DemoContainer, DemoItem } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';

const supportedMinDate = dayjs('2024-01-01')
const supportedMaxDate = dayjs('2025-12-31')
const datePickerLabel = 'Select the game date'

export default function ResponsivePickers({ date, onChange }) {
    return (
        <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DemoContainer components={['DatePicker']}>
                <DemoItem label={datePickerLabel}>
                    <DatePicker defaultValue={date}
                        onChange={onChange}
                        maxDate={supportedMaxDate}
                        minDate={supportedMinDate}
                    />
                </DemoItem>
            </DemoContainer>
        </LocalizationProvider>
    );
}