import * as React from 'react';
import { NumberField } from '@base-ui-components/react/number-field';

export default function NumberInput(prop) {
    return (
        <div className={prop.className}>
            <p>{prop.name}</p>
            <NumberField.Root name={prop.name}
                defaultValue={parseInt(prop.defaultValue)}
                onValueChange={(newVal) => { prop.onValueChange(newVal) }}
                step={0.1}
                min={0}
                max={2}
            >
                <NumberField.Group>
                    <NumberField.Decrement>
                        <MinusIcon />
                    </NumberField.Decrement>
                    <NumberField.Input />
                    <NumberField.Increment>
                        <PlusIcon />
                    </NumberField.Increment>
                </NumberField.Group>
            </NumberField.Root>
        </div>
    );
}


function PlusIcon(props) {
    return (
        <svg
            width="10"
            height="10"
            viewBox="0 0 10 10"
            fill="none"
            stroke="currentcolor"
            strokeWidth="1.6"
            xmlns="http://www.w3.org/2000/svg"
            {...props}
        >
            <path d="M0 5H5M10 5H5M5 5V0M5 5V10" />
        </svg>
    );
}

function MinusIcon(props) {
    return (
        <svg
            width="10"
            height="10"
            viewBox="0 0 10 10"
            fill="none"
            stroke="currentcolor"
            strokeWidth="1.6"
            xmlns="http://www.w3.org/2000/svg"
            {...props}
        >
            <path d="M0 5H10" />
        </svg>
    );
}
