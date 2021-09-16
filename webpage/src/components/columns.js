export const COLUMNS = [
  {
    Header: 'name',
    accessor: 'name'
  },
  {
    Header: 'Short desc',
    accessor: 'description',
    Cell: v =>  v.value.substring(0,15)+"..."
  },
  {
    Header: 'license',
    accessor: 'license'
  },
  {
    Header: 'paper',
    accessor: 'paper',
    Cell: v => (v.value.startsWith("http")===0)
  },
  {
    Header: 'Docker',
    accessor: 'docker',
    Cell: v => (v.value.startsWith("http")===0)

  },
  {
    Header: 'GitHub',
    accessor: 'github',
    Cell: v => (v.value.startsWith("http")===0)
  },
  {
    Header: 'Notebook',
    accessor: 'notebook',
    Cell: v => (v.value.startsWith("http")===0)
  },
  {
    Header: 'Demo',
    accessor: 'demo',
    Cell: v => (v.value.startsWith("http")===0)
  },
  {
    Header: 'Other',
    accessor: 'other'
  }
]
