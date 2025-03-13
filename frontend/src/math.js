export function roundDecimal(val, precision) {
    return Math.round(Math.round(val * Math.pow(10, (precision || 0) + 1)) / 10) / Math.pow(10, (precision || 0)).toFixed(2);
}

export function round(from) {
    console.log('from is', from)
    return Math.round(from * 1000) / 1000
}

export function toPercentageStr(from) {
    if (isNaN(from)) return ''
    from = round(from) * 100
    return from.toFixed(2) + '%'
}

export default {
    round,
    roundDecimal,
    toPercentageStr
}