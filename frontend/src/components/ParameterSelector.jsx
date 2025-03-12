import DatePicker from "./DatePicker"
import NumberInput from './NumberInput'
// import Tooltip from "./Tooltip"

function ParameterSelector(prop) {
    let { page, startDate, endDate, minDate, maxDate,
        setStartDate, setEndDate, weights
    } = prop.requirement

    function renderDatePicker(page) {
        if (page === 'home') {
            return (
                <div className="date-picker-section">
                    {/* <Tooltip /> */}
                    <DatePicker
                        label="Select the game date(ET)"
                        date={startDate}
                        onChange={(newVal) => { setStartDate(newVal) }}
                        minDate={minDate}
                        maxDate={maxDate}
                    />
                </div>
            )
        } else if (page === 'backtest') {
            return (
                <div className="date-picker-section">
                    <DatePicker
                        label="Select the start date(ET)"
                        date={startDate}
                        onChange={(newVal) => { setStartDate(newVal) }}
                        minDate={minDate}
                        maxDate={maxDate}
                        className="start-date"
                    />
                    <DatePicker
                        label="Select the end date(ET)"
                        date={endDate}
                        onChange={(newVal) => { setEndDate(newVal) }}
                        minDate={minDate}
                        maxDate={maxDate}
                        className="end-date"
                    />
                </div>
            )
        }
    }

    return (
        <div className="parameter-selector">
            <div className="parameter-section flex flex-justify-between">
                {renderDatePicker(page)}
                <div className="weight-input-section flex flex-justify-between">
                    {
                        weights.map((weight, wIdx) => {
                            return (
                                <NumberInput
                                    className="flex weight-input flex-column"
                                    name={weight.name}
                                    defaultValue={weight.defaultValue}
                                    onValueChange={weight.setFunction}
                                    key={wIdx}
                                />
                            )
                        })
                    }
                </div>
            </div>

        </div>
    )
}

export default ParameterSelector