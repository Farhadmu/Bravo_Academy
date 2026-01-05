'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
    Database,
    Search,
    Table as TableIcon,
    RefreshCw,
    Download,
    Terminal,
    AlertCircle
} from 'lucide-react';
import api from '@/lib/api';
import { toast } from 'sonner';

interface TableInfo {
    name: string;
    columns: number;
}

interface TableData {
    columns: string[];
    rows: any[];
}

export default function DatabaseInspector() {
    const [tables, setTables] = useState<TableInfo[]>([]);
    const [selectedTable, setSelectedTable] = useState<string | null>(null);
    const [tableData, setTableData] = useState<TableData | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [isTableLoading, setIsTableLoading] = useState(false);

    const fetchTables = async () => {
        setIsLoading(true);
        try {
            const res = await api.get('/system/database/');
            setTables(res.data);
        } catch (error) {
            toast.error('Failed to load database schema');
        } finally {
            setIsLoading(false);
        }
    };

    const fetchTableData = async (tableName: string) => {
        setSelectedTable(tableName);
        setIsTableLoading(true);
        try {
            const res = await api.get(`/system/database/table_data/?table=${tableName}`);
            setTableData(res.data);
        } catch (error) {
            toast.error(`Failed to load data for ${tableName}`);
            setTableData(null);
        } finally {
            setIsTableLoading(false);
        }
    };

    useEffect(() => {
        fetchTables();
    }, []);

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <Database className="h-8 w-8 text-blue-400" />
                        Database Inspector
                    </h1>
                    <p className="text-slate-400 mt-1">Direct read access to system tables. Limited to 100 rows.</p>
                </div>
                <Button variant="outline" onClick={fetchTables} className="bg-slate-900 border-slate-700">
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Refresh
                </Button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                {/* Tables List */}
                <div className="lg:col-span-1 space-y-4">
                    <Card className="bg-slate-900 border-slate-800 text-white min-h-[500px]">
                        <CardHeader className="pb-2">
                            <CardTitle className="text-xs font-mono uppercase tracking-widest text-slate-500">Public Tables</CardTitle>
                        </CardHeader>
                        <CardContent className="p-2">
                            <div className="space-y-1">
                                {tables.map((table) => (
                                    <button
                                        key={table.name}
                                        onClick={() => fetchTableData(table.name)}
                                        className={`w-full text-left px-3 py-2 rounded-md transition-colors flex items-center justify-between ${selectedTable === table.name
                                                ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
                                                : 'text-slate-400 hover:bg-slate-800'
                                            }`}
                                    >
                                        <div className="flex items-center gap-2 overflow-hidden">
                                            <TableIcon className="h-4 w-4 flex-shrink-0" />
                                            <span className="truncate text-sm font-mono">{table.name}</span>
                                        </div>
                                        <span className="text-[10px] bg-slate-800 px-1.5 py-0.5 rounded text-slate-500">{table.columns}</span>
                                    </button>
                                ))}
                            </div>
                        </CardContent>
                    </Card>
                </div>

                {/* Table Data View */}
                <div className="lg:col-span-3">
                    <Card className="bg-slate-900 border-slate-800 text-white min-h-[500px] flex flex-col">
                        <CardHeader className="border-b border-slate-800 flex flex-row items-center justify-between">
                            <div>
                                <CardTitle className="font-mono text-xl">{selectedTable || 'Select a Table'}</CardTitle>
                                {selectedTable && <CardDescription className="text-slate-500">Showing first {tableData?.rows.length || 0} records</CardDescription>}
                            </div>
                            {tableData && (
                                <Button variant="ghost" size="sm" className="text-slate-400 hover:text-white">
                                    <Download className="h-4 w-4 mr-2" />
                                    Export JSON
                                </Button>
                            )}
                        </CardHeader>
                        <CardContent className="p-0 flex-grow overflow-auto">
                            {isTableLoading ? (
                                <div className="flex items-center justify-center h-full p-20">
                                    <RefreshCw className="h-8 w-8 text-blue-500 animate-spin" />
                                </div>
                            ) : tableData ? (
                                <div className="relative overflow-x-auto">
                                    <table className="w-full text-sm text-left text-slate-400">
                                        <thead className="text-xs text-slate-500 uppercase bg-slate-950/50 sticky top-0">
                                            <tr>
                                                {tableData.columns.map((col) => (
                                                    <th key={col} scope="col" className="px-6 py-3 border-b border-slate-800 font-mono">
                                                        {col}
                                                    </th>
                                                ))}
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {tableData.rows.map((row, idx) => (
                                                <tr key={idx} className="bg-slate-900 hover:bg-slate-800/50 border-b border-slate-800 transition-colors">
                                                    {tableData.columns.map((col) => (
                                                        <td key={col} className="px-6 py-4 font-mono text-[11px] whitespace-nowrap">
                                                            {row[col] === null ? (
                                                                <span className="text-slate-700 italic">null</span>
                                                            ) : typeof row[col] === 'object' ? (
                                                                <span className="text-yellow-500/70">{JSON.stringify(row[col]).substring(0, 30)}...</span>
                                                            ) : (
                                                                String(row[col])
                                                            )}
                                                        </td>
                                                    ))}
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            ) : (
                                <div className="flex flex-col items-center justify-center h-full p-20 text-slate-600">
                                    <Search className="h-16 w-16 mb-4 opacity-20" />
                                    <p className="text-lg font-medium opacity-50">Select a table from the sidebar to inspect its content</p>
                                </div>
                            )}
                        </CardContent>
                    </Card>

                    {/* Security Info */}
                    <div className="mt-4 p-4 bg-blue-950/20 border border-blue-900/40 rounded-lg flex gap-3">
                        <AlertCircle className="h-5 w-5 text-blue-400 flex-shrink-0" />
                        <div className="text-xs text-blue-300">
                            <p className="font-bold uppercase tracking-widest mb-1">Developer Notice</p>
                            <p>This is a read-only view of the database. For security reasons, DELETE, UPDATE, and raw EXECUTE commands are disabled in this interface. Use the terminal or migrations for data modification.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
