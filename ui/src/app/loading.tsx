import { Loading as LoadingComponent } from '@/components/layout/content/Loading';

const Loading = async () => (
  <>
    <div className="content-wrapper">{<LoadingComponent />}</div>
  </>
);

export default Loading;