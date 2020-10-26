function get_date() {
  const d = new Date();
  const ye = new Intl.DateTimeFormat("en-US", { year: "numeric" }).format(d);
  const mo = new Intl.DateTimeFormat("en-US", { month: "short" }).format(d);
  const da = new Intl.DateTimeFormat("en-US", { day: "numeric" }).format(d);

  formatted_date = `${mo} ${da}`;
  console.log(formatted_date);
  return formatted_date;
}
