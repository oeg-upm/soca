import React, { useMemo } from 'react'
import { useTable, useGlobalFilter } from 'react-table'
import CATALOG_DATA from './catalog_mini.json'
import { COLUMNS } from './columns'
import './table.css'
import { GlobalFilter } from './GlobalFilter'

export const FilteringTable = () => {

  const columns = useMemo(() => COLUMNS, [])
  const data = useMemo(() => CATALOG_DATA, [])

  const getLink = (url) => {
    if (url.startsWith("http")){
      return '<a href="'+url+'">'
    }
    return ''
  }

  const getEndLink = (url) => {
    if (url.startsWith("http")){
      return '</a>'
    }
    return ''
  }

  const getColor = (quantity) => {
    if (quantity == ''){
      return 'red'
    } else {
      if (quantity.startsWith("http")){
        return 'green'
      } else {
        return ''
      }
    }
  };

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    footerGroups,
    rows,
    prepareRow,
    state,
    setGlobalFilter
  } = useTable(
    {
      columns,
      data
    },
    useGlobalFilter
  )

  const { globalFilter } = state

  return (
    <>
    <GlobalFilter filter={globalFilter} setFilter={ setGlobalFilter }/>
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
                    return (<td style={{ background: getColor(cell.value) }}>{cell.render('Cell')}</td>)
                    //cell.render('Cell')
                  })
                }
              </tr>
            )
          })
        }
      </tbody>
    </table>
    </>
  )
}
