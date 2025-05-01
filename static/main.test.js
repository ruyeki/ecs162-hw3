const { showDate } = require('./main');

describe('showDate', () => {
    beforeEach(() => {
        document.body.innerHTML = `<div id="date"></div>`;
    });

    // Check for correct format.
    test('formats date correctly', () => {
        const testDate = new Date(2025, 4, 1);
        const result = showDate(testDate);
        expect(result).toBe('Thursday May 1, 2025');
        expect(document.getElementById('date').innerHTML).toContain('Thursday May 1, 2025');
    });

    // Checks for leap year
    test('formats leap year date correctly', () => {
        const date = new Date(2024, 1, 29);
        const result = showDate(date);
        expect(result).toBe('Thursday February 29, 2024');
    });
});
