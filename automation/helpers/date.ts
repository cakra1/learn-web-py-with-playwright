export function formatDateDMY(input: any): string {
  // 1️⃣ Kalau Excel ngirim Date object
  if (input instanceof Date) {
    const d = String(input.getDate()).padStart(2, '0');
    const m = String(input.getMonth() + 1).padStart(2, '0');
    const y = input.getFullYear();
    return `${d}/${m}/${y}`;
  }

  // 2️⃣ Kalau string
  const value = String(input).trim();

  // yyyy-mm-dd → dd/mm/yyyy
  if (/^\d{4}-\d{2}-\d{2}$/.test(value)) {
    const [y, m, d] = value.split('-');
    return `${d}/${m}/${y}`;
  }

  // dd-mm-yyyy → dd/mm/yyyy
  if (/^\d{2}-\d{2}-\d{4}$/.test(value)) {
    return value.replace(/-/g, '/');
  }

  // dd/mm/yyyy → biarin
  if (/^\d{2}\/\d{2}\/\d{4}$/.test(value)) {
    return value;
  }

  // 3️⃣ Kalau aneh → fail fast (BEST PRACTICE)
  throw new Error(`Invalid date format from Excel: ${input}`);
}
