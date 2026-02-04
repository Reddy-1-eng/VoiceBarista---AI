import * as React from 'react';
import { cn } from '@/lib/utils';

export interface ChatEntryProps extends React.HTMLAttributes<HTMLLIElement> {
  /** The locale to use for the timestamp. */
  locale: string;
  /** The timestamp of the message. */
  timestamp: number;
  /** The message to display. */
  message: string;
  /** The origin of the message. */
  messageOrigin: 'local' | 'remote';
  /** The sender's name. */
  name?: string;
  /** Whether the message has been edited. */
  hasBeenEdited?: boolean;
}

export const ChatEntry = ({
  name,
  locale,
  timestamp,
  message,
  messageOrigin,
  hasBeenEdited = false,
  className,
  ...props
}: ChatEntryProps) => {
  const time = new Date(timestamp);
  const title = time.toLocaleTimeString(locale, { timeStyle: 'full' });

  return (
    <li
      title={title}
      data-lk-message-origin={messageOrigin}
      className={cn('group flex w-full flex-col gap-2 mb-4', className)}
      {...props}
    >
      <header
        className={cn(
          'flex items-center gap-2 text-sm font-medium',
          messageOrigin === 'local' 
            ? 'flex-row-reverse text-blue-600' 
            : 'text-amber-600'
        )}
      >
        {messageOrigin === 'local' ? (
          <div className="flex items-center gap-2">
            <span className="text-blue-600 font-semibold">👤 You</span>
          </div>
        ) : (
          <div className="flex items-center gap-2">
            <span className="text-amber-600 font-semibold">☕ AgentX Barista</span>
          </div>
        )}
        <span className="font-mono text-xs text-gray-500 opacity-0 transition-opacity ease-linear group-hover:opacity-100">
          {hasBeenEdited && '*'}
          {time.toLocaleTimeString(locale, { timeStyle: 'short' })}
        </span>
      </header>
      <div
        className={cn(
          'max-w-[85%] rounded-2xl px-4 py-3 shadow-sm border',
          messageOrigin === 'local' 
            ? 'bg-blue-500 text-white ml-auto border-blue-400' 
            : 'bg-white text-gray-800 mr-auto border-gray-200 shadow-md'
        )}
      >
        <span className="text-sm leading-relaxed whitespace-pre-wrap">
          {message}
        </span>
      </div>
    </li>
  );
};
