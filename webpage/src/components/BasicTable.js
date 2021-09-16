import React, { useMemo } from 'react'
import { useTable } from 'react-table'
import CATALOG_DATA from './catalog.json'
import { COLUMNS } from './columns'
import './table.css'

export const BasicTable = () => {

  const columns = useMemo(() => COLUMNS, [])
  const data = useMemo(() => CATALOG_DATA, [])

  const tableInstance = useTable({
    columns,
    data
  })

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = tableInstance

  return (
    <table {...getTableProps()}>
    <thead>
        {headerGroups.map(headerGroup => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map(column => (
              <th {...column.getHeaderProps()}>{column.render('Header')}</th>
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
