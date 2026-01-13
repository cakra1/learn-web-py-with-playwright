import { test, expect } from '@playwright/test';
import { readExcel } from '../helpers/readExcel';
import { register } from '../helpers/register';

const data = readExcel('excel/registration.xlsx');

for (const row of data as any[]) {
  test(`register ${row.email} - ${row.expected}`, async ({ page }) => {
  await register(page, row);

  if (row.expected === 'success') {
    await expect(page).not.toHaveURL(/index-peserta/);
  } else {
    await expect(page).toHaveURL(/index-peserta/);
  }

  await page.waitForTimeout(3000);
  });
}
