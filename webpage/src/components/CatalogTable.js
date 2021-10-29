import { Table, Tag, Space, Tooltip } from 'antd';
import 'antd/dist/antd.css';
import CATALOG_DATA from './catalog.json'
import SOMEF_DATA from './widoco.json'
import { COLUMNS } from './columns'
import React, { useMemo } from 'react'
import ReactDOM from 'react-dom';
import MarkdownPreview from '@uiw/react-markdown-preview';

export const CatalogTable = () => {
//render: text => <p>{text[0].excerpt}</p>,
  const columns = [
    {
      key: 'name',
      title: 'Name',
      dataIndex: 'long_title',
      render: text => <MarkdownPreview source={text.excerpt} />,
    },
    {
      key: 'license',
      title: 'License',
      dataIndex: 'license',
      filters: [
        {
          text:'Other',
          value:'Other'
        },
        {
          text:'MIT',
          value:'MIT'
        },
      ],
      onFilter: (value, record) => record.license.excerpt.name.indexOf(value) >= 0,
      filterSearch: true,
      render: text => <a href={text.excerpt.url}>{text.excerpt.name}</a>,
    },
    {
      key: 'paper',
      title: 'Paper',
      dataIndex: 'citation',
      ellipsis: {
        showTitle: false,
      },
      render: text => (
        <Tooltip placement="topLeft" title={text[0].excerpt}>
          {text[0].excerpt}
        </Tooltip>
      ),
    },
    {
      key: 'code',
      title: 'Code',
      dataIndex: 'codeRepository',
      render: text => <a href={text.excerpt}><img src="../../github-logo.png"></img></a>,
    },
    {
      key: 'usage',
      title: 'Usage',
      dataIndex: 'usage',
      render: list => (
      <>
        {list.map(element => {
          let text = element.excerpt.substring(0,20)+'...'
          return (
            <p>
              <Tooltip placement="topLeft" title={element.excerpt}>
                <Tag color='green' key='usage'>Usage</Tag>
              </Tooltip>
            </p>
          );
        })}
      </>
      ),
    },
    {
      key: 'demo',
      title: 'Demo / Notebook',
      dataIndex: 'executable_example',
      render: list => (
        <>
          {list!=undefined &&
            list.map(element => {
              return(
                <a href={element.excerpt}>
                  <Tag color='blue' key='usage'>MyBinder</Tag>
                </a>
              );
            })
          }
        </>
      ),
    },
    {
      key: 'docker',
      title: 'Docker',
      dataIndex: ['hasBuildFile','excerpt'],
      render: list => (
        <>
          { list!=undefined  &&
            list.map(element => {
              return(
                <a href={element}>
                  <Tag color='black' key='docker'>Docker</Tag>
                </a>
              );
            })
          }
        </>
      ),
    },
    {
      key: 'installation',
      title: 'Installation',
      dataIndex: 'installation',
      render: list => (
        <>
          { list!=undefined &&
            list.map(element => {
              return(
                <Tooltip placement="topLeft" title={element.excerpt}>
                  <Tag color='green' key='usage'>Recipe</Tag>
                </Tooltip>
              );
            })
          }
        </>
      ),
    },
  ];

const data = useMemo(() => SOMEF_DATA, [])

function onChange(pagination, filters, sorter, extra) {
  console.log('params', pagination, filters, sorter, extra);
}

return (
  <Table columns={columns} dataSource={data} bordered
    title={() => 'Software Catalog'}
    footer={() => 'Ontology Engineering Group'}
    expandable={{
      expandedRowRender: record => <MarkdownPreview source={record.description[0].excerpt} />,
    }}
    onChange={onChange}
    rowkey={(record) => record.long_title.excerpt} />
)

}
