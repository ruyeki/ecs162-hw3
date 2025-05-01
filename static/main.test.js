const { showDate } = require('./main');

describe('showDate', () => {
    beforeEach(() => {
        document.body.innerHTML = `<div id="date"></div>`;
    });

    test('formats date correctly', () => {
        const testDate = new Date(2024, 6, 4); // July 4, 2024
        const result = showDate(testDate);
        expect(result).toBe('Thursday July 4, 2024');
        expect(document.getElementById('date').innerHTML).toContain('Thursday July 4, 2024');
    });
});
