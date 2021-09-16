import React, { useMemo } from 'react'
import { useTable, useSortBy } from 'react-table'
import CATALOG_DATA from './catalog.json'
import { COLUMNS } from './columns'
import './table.css'

export const SortingTable = () => {

  const columns = useMemo(() => COLUMNS, [])
  const data = useMemo(() => CATALOG_DATA, [])

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    footerGroups,
    rows,
    prepareRow
  } = useTable(
    {
      columns,
      data
    },
    useSortBy
  )

  return (
    <table {...getTableProps()}>
    <thead>
        {headerGroups.map(headerGroup => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map(column => (
              <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                  {column.render('Header')}
                  <span>
                    {column.isSorted
                      ? column.isSortedDesc
                        ? ' 🔽'
                        : ' 🔼'
                      : ''}
                  </span>
                </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody {...getTableBodyProps()}>
        {
          rows.map(row => {
            prepareRow(row)
            return (
              <tr {...row.getRowProps()}>
                {
                  row.cells.map(cell =>{
                    return (<td {...cell.getCellProps()}>{cell.render('Cell')}</td>)
                  })
                }
              </tr>
            )
          })
        }
      </tbody>
    </table>
  )
}
