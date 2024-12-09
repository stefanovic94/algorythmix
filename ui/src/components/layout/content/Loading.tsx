import { UpdateIcon } from '@radix-ui/react-icons';

interface Props {
  text?: string;
}

export const Loading = async ({ text }: Props) => (
  <div className={`flex items-center`}>
    <UpdateIcon className="m-2 animate-spin" /> {text}
  </div>
);

const loadingHandler = (text: string) => {
  const LoadingComponent = async () => {
    return <Loading text={text} />;
  };
  return LoadingComponent;
};

export default loadingHandler;