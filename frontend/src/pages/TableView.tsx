import { useState, useEffect } from 'react';

export default function TableView() {
  const [items, setItems] = useState<any[]>([]);
  
  useEffect(() => {
    fetch('/api/mortality?page=1&limit=20')
      .then(r => r.json())
      .then(setItems)
      .catch(() => {});
  }, []);
  
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Mortality Records</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full border">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-2 text-left">Country</th>
              <th className="px-4 py-2 text-left">Year</th>
              <th className="px-4 py-2 text-left">Age Group</th>
              <th className="px-4 py-2 text-left">Sex</th>
              <th className="px-4 py-2 text-left">Deaths</th>
              <th className="px-4 py-2 text-left">Rate</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item, i) => (
              <tr key={i} className="border-t">
                <td className="px-4 py-2">{item.country_name}</td>
                <td className="px-4 py-2">{item.year}</td>
                <td className="px-4 py-2">{item.age_group}</td>
                <td className="px-4 py-2">{item.sex}</td>
                <td className="px-4 py-2">{item.deaths}</td>
                <td className="px-4 py-2">{item.death_rate}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
