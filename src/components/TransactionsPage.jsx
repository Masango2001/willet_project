// import React from 'react';
// import { ArrowLeft, Send, ArrowDownLeft } from 'lucide-react';

// const TransactionsPage = ({ onBack }) => {
//   const transactions = [
//     { id: 1, type: 'receive', amount: 0.5, address: '1A2B3C4D5E6F7G8H9I0J', date: '2024-08-06', time: '14:30', status: 'confirmed' },
//     { id: 2, type: 'send', amount: -0.2, address: '4D5E6F7G8H9I0J1A2B3C', date: '2024-08-05', time: '09:15', status: 'confirmed' },
//     { id: 3, type: 'receive', amount: 1.0, address: '7G8H9I0J1A2B3C4D5E6F', date: '2024-08-03', time: '16:45', status: 'confirmed' },
//     { id: 4, type: 'send', amount: -0.1, address: '9I0J1A2B3C4D5E6F7G8H', date: '2024-08-02', time: '11:20', status: 'pending' },
//   ];

//   return (
//     <div className="centered-container" style={{
//       background: 'linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e40af 100%)'
//     }}>
//       <div className="px-6 py-8 centered-content">
//         {/* Header */}
//         <div className="flex items-center mb-8">
//           <button
//             onClick={onBack}
//             className="p-2 text-white hover:bg-gray-800 rounded-lg transition-all duration-200"
//           >
//             <ArrowLeft size={24} />
//           </button>
//           <h1 className="text-white text-xl font-bold ml-4">Transaction History</h1>
//         </div>

//         <div className="space-y-4">
//           {transactions.map((tx) => (
//             <div key={tx.id} className="bg-gray-800 p-4 rounded-xl">
//               <div className="flex items-center justify-between mb-3">
//                 <div className="flex items-center gap-3">
//                   <div className={`p-2 rounded-full ${
//                     tx.type === 'receive' 
//                       ? 'bg-green-500/20 text-green-400' 
//                       : 'bg-red-500/20 text-red-400'
//                   }`}>
//                     {tx.type === 'receive' ? <ArrowDownLeft size={16} /> : <Send size={16} />}
//                   </div>
//                   <div>
//                     <div className="text-white font-medium capitalize">{tx.type}</div>
//                     <div className={`text-sm px-2 py-1 rounded ${
//                       tx.status === 'confirmed' 
//                         ? 'bg-green-500/20 text-green-400' 
//                         : 'bg-yellow-500/20 text-yellow-400'
//                     }`}>
//                       {tx.status}
//                     </div>
//                   </div>
//                 </div>
//                 <div className="text-right">
//                   <div className={`font-semibold text-lg ${
//                     tx.amount > 0 ? 'text-green-400' : 'text-red-400'
//                   }`}>
//                     {tx.amount > 0 ? '+' : ''}{tx.amount} BTC
//                   </div>
//                   <div className="text-gray-400 text-sm">
//                     ≈ ${Math.abs(tx.amount * 40000).toLocaleString()}
//                   </div>
//                 </div>
//               </div>
//               <div className="border-t border-gray-700 pt-3">
//                 <div className="flex justify-between text-sm text-gray-400">
//                   <span>Address: {tx.address}</span>
//                   <span>{tx.date} {tx.time}</span>
//                 </div>
//               </div>
//             </div>
//           ))}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default TransactionsPage;