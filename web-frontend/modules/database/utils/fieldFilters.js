// We can't use the humanReadable value here as:
// A: it contains commas which we don't want to match against
// B: even if we removed the commas and compared filterValue against the concatted
//    list of file names, we don't want the filterValue to accidentally match the end
//    of one filename and the start of another.
export function filenameContainsFilter(
  rowValue,
  humanReadableRowValue,
  filterValue
) {
  filterValue = filterValue.toString().toLowerCase().trim()

  for (let i = 0; i < rowValue.length; i++) {
    const visibleName = rowValue[i].visible_name.toString().toLowerCase().trim()

    if (visibleName.includes(filterValue)) {
      return true
    }
  }

  return false
}

export function genericContainsFilter(
  rowValue,
  humanReadableRowValue,
  filterValue
) {
  if (humanReadableRowValue == null) {
    return false
  }
  humanReadableRowValue = humanReadableRowValue.toString().toLowerCase().trim()
  filterValue = filterValue.toString().toLowerCase().trim()
  return humanReadableRowValue.includes(filterValue)
}

export function genericContainsWordFilter(
  rowValue,
  humanReadableRowValue,
  filterValue
) {
  if (humanReadableRowValue == null) {
    return false
  }
  humanReadableRowValue = humanReadableRowValue.toString().toLowerCase().trim()
  filterValue = filterValue.toString().toLowerCase().trim()
  // check using regex to match whole words
  // make sure to escape the filterValue as it may contain regex special characters
  filterValue = filterValue.replace(/[-[\]{}()*+?.,\\^$|#]/g, '\\$&')
  return humanReadableRowValue.match(new RegExp(`\\b${filterValue}\\b`))
}
