export function applyDateMask() {
    document.getElementById('date-mask').addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        
        let formattedValue = '';
        if (value.length > 0) formattedValue += value.substring(0, 4);
        if (value.length > 4) formattedValue += '-' + value.substring(4, 6);
        if (value.length > 6) formattedValue += '-' + value.substring(6, 8);
        if (value.length > 8) formattedValue += ' ' + value.substring(8, 10);
        if (value.length > 10) formattedValue += ':' + value.substring(10, 12);
        if (value.length > 12) formattedValue += ':' + value.substring(12, 14);
        
        e.target.value = formattedValue;
    });
}