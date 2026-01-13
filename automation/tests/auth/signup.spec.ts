import { test, expect } from '@playwright/test';
import { readExcel } from '../helpers/readExcel';
import { signup } from '../helpers/signup';

const data = readExcel('excel/signup.xlsx');

for (const row of data as any[]) {
  test(`signup ${row.Email}`, async ({ page }) => {
    await signup(page, row);

    if (row.Expected === 'success') {
      await expect(page).toHaveURL(/peserta|admin|login/);
    } else {
      await expect(page.locator('.alert-danger')).toBeVisible();
    }

  });
}
